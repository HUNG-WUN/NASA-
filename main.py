import networkx as nx
import matplotlib.pyplot as plt
import json
import random
import argparse


# ========== 拓撲生成 ==========
def generate_hypercube(dimension: int):
    G = nx.hypercube_graph(dimension)
    mapping = {node: i for i, node in enumerate(G.nodes())}
    return nx.relabel_nodes(G, mapping)


def generate_twisted_cube(dimension: int):
    G = generate_hypercube(dimension)
    nodes = list(G.nodes)
    for node in nodes:
        if node % 2 == 1:
            neighbor = (node + 2) % len(nodes)
            G.add_edge(node, neighbor)
    return G


def generate_crossed_cube(dimension: int):
    G = generate_hypercube(dimension)
    nodes = list(G.nodes)
    for node in nodes:
        cross_node = len(nodes) - 1 - node
        if not G.has_edge(node, cross_node):
            G.add_edge(node, cross_node)
    return G


# ========== 節點失效模擬 ==========
def simulate_node_failure(G, fail_rate=0.1, seed=None):
    if seed is not None:
        random.seed(seed)
    num_fail = int(len(G.nodes) * fail_rate)
    return random.sample(list(G.nodes), num_fail)


# ========== 視覺化 ==========
def visualize_topology(G, failed_nodes=None, title="Topology"):
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=[n for n in G.nodes if n not in failed_nodes],
        node_color="skyblue", node_size=600
    )
    if failed_nodes:
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=failed_nodes,
            node_color="red", node_size=600
        )
    nx.draw_networkx_edges(G, pos, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")
    plt.title(title)
    plt.axis("off")
    plt.show()


# ========== 匯出模擬規格 ==========
def export_spec(G, failed_nodes, topology_name, filename="week1_spec.json"):
    spec = {
        "topology": topology_name,
        "num_nodes": len(G.nodes),
        "num_edges": len(G.edges),
        "failed_nodes": failed_nodes,
        "evaluation_metrics": [
            "average_delay",
            "delivery_rate",
            "diagnosis_accuracy",
            "energy_consumption"
        ]
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=4)
    print(f"[INFO] 規格已輸出到 {filename}")


# ========== 主程式 ==========
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Week1: DTN Topology Simulation")
    parser.add_argument("--topology", type=str, default="hypercube",
                        choices=["hypercube", "twisted", "crossed"],
                        help="選擇拓撲類型")
    parser.add_argument("--dimension", type=int, default=4,
                        help="Hypercube 維度 (節點數 = 2^dimension)")
    parser.add_argument("--fail_rate", type=float, default=0.2,
                        help="節點失效比例 (0~1)")
    parser.add_argument("--output", type=str, default="week1_spec.json",
                        help="輸出 JSON 檔名")
    parser.add_argument("--seed", type=int, default=42,
                        help="隨機種子 (方便重現)")

    args = parser.parse_args()

    # ====== 生成拓撲 ======
    if args.topology == "hypercube":
        G = generate_hypercube(args.dimension)
    elif args.topology == "twisted":
        G = generate_twisted_cube(args.dimension)
    elif args.topology == "crossed":
        G = generate_crossed_cube(args.dimension)
    else:
        raise ValueError("未知的拓撲類型")

    # ====== 模擬節點失效 ======
    failed_nodes = simulate_node_failure(G, args.fail_rate, seed=args.seed)

    # ====== 視覺化 ======
    visualize_topology(G, failed_nodes,
                       title=f"{args.topology.capitalize()} (d={args.dimension})")

    # ====== 輸出規格 ======
    export_spec(G, failed_nodes, topology_name=args.topology,
                filename=args.output)
