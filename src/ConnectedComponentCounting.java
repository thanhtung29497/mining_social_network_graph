import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;

public class ConnectedComponentCounting {
	private Graph graph;
	private Set<String> tempConnectedComponent;
	private HashSet<String> visitedNode;
	
	private void dfs(String targetNode) {
		if (this.visitedNode.contains(targetNode)) {
			return;
		}
		this.visitedNode.add(targetNode);
		this.tempConnectedComponent.add(targetNode);
		
		for (String neighbor: this.graph.getNeighborNodes(targetNode)) {
			this.dfs(neighbor);
		}
	}
	
	public List<Set<String>> getResult() {
		List<Set<String>> result = new LinkedList<>();
		this.tempConnectedComponent = new HashSet<>();
		
		for (String node: this.graph.getNodes()) {
			if (!this.visitedNode.contains(node)) {
				
				this.tempConnectedComponent = new HashSet<>();
				this.dfs(node);
				result.add(this.tempConnectedComponent);
				
			}
		}
		
		return result;
	}
	
	public ConnectedComponentCounting(Graph graph) {
		this.graph = graph;
		this.visitedNode = new HashSet<>();
	}
	
	public static void main(String[] argv) {
		
		try {
			
			Graph graph = Graph.loadGraphFromFile(Graph.GRAPH_INPUT_FILE_DIR);
			
			ConnectedComponentCounting counting = new ConnectedComponentCounting(graph);
			List<Set<String>> connectedComponents = counting.getResult();
			int count = 1;
			for (Set<String> connectedComponent: connectedComponents) {
				System.out.println("Connected component " + count + ": ");
				for (String node: connectedComponent) {
					System.out.println(node);
				}
				count++;
			}
			
			
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} 
		  
		
	}
}
