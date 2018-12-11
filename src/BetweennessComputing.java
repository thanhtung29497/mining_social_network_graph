import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;

public class BetweennessComputing {
	private Graph graph;
	private HashMap<String, Integer> degree;
	private HashMap<String, Integer> shortestPathNumber;
	private HashMap<String, HashSet<String>> reversePaths;
	private HashMap<String, Double> betweenness;
	private HashMap<String, Double> nodeValues;
	private LinkedList<String> reverseNodes;
	public static final String EDGE_DELIMETER = "-";
	
	public BetweennessComputing(Graph graph) {
		this.graph = graph;
	}
	
	private void addReversePath(String origin, String destination) {
		HashSet<String> reversePaths;
		if (!this.reversePaths.containsKey(destination)) {
			reversePaths = new HashSet<>();
		} else {
			reversePaths = this.reversePaths.get(destination);
		}
		reversePaths.add(origin);
		
		this.reversePaths.put(destination, reversePaths);
	}
	
	public void compute() {
		this.betweenness = new HashMap<>();
		for (String node: this.graph.getNodes()) {
			this.calShortestPathNumber(node);
			this.reverse(node);
		}
		
		for (String edge: this.betweenness.keySet()) {
			System.out.println(edge + ": " + this.betweenness.get(edge));
		}
		
		Double maxBetweenness = 0.0;
		for (Double value: this.betweenness.values()) {
			maxBetweenness = Math.max(maxBetweenness, value);
		}
		System.out.println(maxBetweenness);
		
	}
	
	public void calShortestPathNumber(String root) {
		Queue<String> openSet = new LinkedList<>();
		this.degree = new HashMap<>();
		this.shortestPathNumber = new HashMap<>();
		this.reverseNodes = new LinkedList<>();
		this.nodeValues = new HashMap<>();
		this.reversePaths = new HashMap<>();
		
		openSet.add(root);
		this.shortestPathNumber.put(root, 1);
		this.degree.put(root, 0);
		
		while (!openSet.isEmpty()) {
			
			String currentNode = openSet.poll();
			Integer currentDegree = this.degree.get(currentNode);
			Integer currentShortestPathNumber = this.shortestPathNumber.get(currentNode);
			Boolean isLeafNode = true;
			
			for (String neighbor: this.graph.getNeighborNodes(currentNode)) {
				
				if (!this.degree.containsKey(neighbor)) {
					
					this.degree.put(neighbor, currentDegree + 1);
					this.shortestPathNumber.put(neighbor, currentShortestPathNumber);
					openSet.add(neighbor);
					this.addReversePath(currentNode, neighbor);
					isLeafNode = false;
					
				} else if (this.degree.get(neighbor) == currentDegree + 1) {
					
					this.shortestPathNumber.put(neighbor, 
							this.shortestPathNumber.get(neighbor) + currentShortestPathNumber);
					this.addReversePath(currentNode, neighbor);
					isLeafNode = false;
					
				}
			}
			
			if (isLeafNode) {
				this.reverseNodes.add(currentNode);
			} 
			this.nodeValues.put(currentNode, 1.0);
		}
	}
	
	private void addBetweenness(String node1, String node2, Double value) {
		String edge = node1 + BetweennessComputing.EDGE_DELIMETER + node2;
		if (!this.betweenness.containsKey(edge)) {
			this.betweenness.put(edge, value);
		} else {
			this.betweenness.put(edge, this.betweenness.get(edge) + value);
		}
	}
	
	private void reverse(String root) {
		
		HashSet<String> addedNodes = new HashSet<>();
		
		while (!this.reverseNodes.isEmpty()) {
			String currentNode = this.reverseNodes.poll();
			Double currentNodeValues = this.nodeValues.get(currentNode);
			Integer currentShortestPath = this.shortestPathNumber.get(currentNode);
			if (!this.reversePaths.containsKey(currentNode)) {
				break;
			}
			
			for (String parent: this.reversePaths.get(currentNode)) {
				Double fractionShortestPathValue = 1.0 * this.shortestPathNumber.get(parent) / currentShortestPath;
				this.addBetweenness(currentNode, parent, 
						fractionShortestPathValue * currentNodeValues);
				this.nodeValues.put(parent, this.nodeValues.get(parent) + 
						fractionShortestPathValue * currentNodeValues);
				if (!addedNodes.contains(parent)) {
					this.reverseNodes.add(parent);
					addedNodes.add(parent);
				}
			}
		}
	}
	
	public static void main(String[] argv) {
		try {
			Graph graph = Graph.loadGraphFromFile(Graph.GRAPH_INPUT_FILE_DIR);
			BetweennessComputing computing = new BetweennessComputing(graph);
			
			computing.compute();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
}
