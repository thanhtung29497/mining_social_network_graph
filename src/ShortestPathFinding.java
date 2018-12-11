import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Map;
import java.util.Queue;
import java.util.Set;

public class ShortestPathFinding {
	
	private Graph graph;
	
	public ShortestPathFinding(Graph graph) {
		this.graph = graph;
	}
	
	public LinkedList<String> find(String origin, String destination) {
		LinkedList<String> path = new LinkedList<>();
		Set<String> closeSet = new HashSet<>();
		Queue<String> openSet = new LinkedList<>();
		Map<String, String> trace = new HashMap<>();
		
		openSet.add(origin);
		closeSet.add(origin);
		
		while (!openSet.isEmpty()) {
			
			String pendingNode = openSet.poll();
			
			if (pendingNode.equals(destination)) {
				path.addFirst(destination);
				String traceBackNode = destination;
				while (!traceBackNode.equals(origin)) {
					traceBackNode = trace.get(traceBackNode);
					path.addFirst(traceBackNode);
				}
				return path;
			}
			
			for (String neighbor: this.graph.getNeighborNodes(pendingNode)) {
				if (!closeSet.contains(neighbor)) {
					openSet.add(neighbor);
					closeSet.add(neighbor);
					trace.put(neighbor, pendingNode);
				}
			}
		}
		
		
		return path;
	}
	
	public static void main(String[] argv) {
		try {
			
			Graph graph = Graph.loadGraphFromFile(Graph.GRAPH_INPUT_FILE_DIR);
			ShortestPathFinding pathFinding = new ShortestPathFinding(graph);
			
			String origin = argv[0];
			String destination = argv[1];
			LinkedList<String> path = pathFinding.find(origin, destination);
			for (String node: path) {
				System.out.print(node);
				if (!path.peekLast().equals(node)) {
					System.out.print(" -> ");
				}
			}
			
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
}
