import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Set;

public class Graph {
	
	public static final String GRAPH_INPUT_FILE_DIR = 
			System.getProperty("user.dir") + "//input//sgb-words.txt";
	
	private HashMap<String, LinkedList<String>> adjacencyLists;
	
	public Graph() {
		this.adjacencyLists = new HashMap<>();
	}
	
	public static Graph loadGraphFromFile(String fileDir) throws IOException {
		File inputFile = new File(fileDir); 
		  
		BufferedReader bufferReader = new BufferedReader(new FileReader(inputFile));
		String inputNode; 
		Graph graph = new Graph();
		
		while ((inputNode = bufferReader.readLine()) != null) {
		    graph.addNode(inputNode); 
		}
		
		bufferReader.close();
		return graph;
	}
	
	public void addNode(String node) {
		LinkedList<String> neighborNodes = new LinkedList<>();
		
		for (String otherNode: this.adjacencyLists.keySet()) {
			if (Graph.isConnected(otherNode, node)) {
				neighborNodes.add(otherNode);
				LinkedList<String> otherNeighborNodes = this.getNeighborNodes(otherNode);
				otherNeighborNodes.add(node);
				this.adjacencyLists.put(otherNode, otherNeighborNodes);
			}
		}
		
		this.adjacencyLists.put(node, neighborNodes);
		
	}
	
	public Set<String> getNodes() {
		return this.adjacencyLists.keySet();
	}
	
	public LinkedList<String> getNeighborNodes(String node) {
		return this.adjacencyLists.get(node);
	}
	
	public static boolean isConnected(String node1, String node2) {
		int difference = 0;
		for (int index = 0; index < node1.length(); ++index) {
			if (node1.charAt(index) != node2.charAt(index)) {
				difference++;
			}
		}
		return difference == 1;
	}
}
