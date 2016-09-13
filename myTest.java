package net.datastructures;

import net.datastructures.AVLTree.AVLNode;



public class MyTest<K,V> extends BinarySearchTree{
	
	/*
	public static<K,V> void inorderTraversal(Position<Entry<Integer, String>> position){
		
		if(position.getLeft()!=null){
			inorderTraversal(position.getLeft());
		}
		System.out.println(position.element().getKey());
		System.out.println(position.element().getValue());
		if(position.getRight()!=null){
			inorderTraversal((AVLNode<K, V>) position.getRight());
		} 
	}
	*/
	public Iterable<Position<Entry<K,V>>> positions2() {
		   PositionList<Position<Entry<K,V>>> positions = new NodePositionList<Position<Entry<K,V>>>();
		    if(size != 0)
		      inorderPositions(root(), positions);  // assign positions in inorder, the time complexity is O(n)
		    return positions;
	}	

	public Iterable<Entry<K,V>> inorderEntries() {
		PositionList<Entry<K,V>> entries = new NodePositionList<Entry<K,V>>();
		Iterable<Position<Entry<K,V>>> positer = positions2();
		for (Position<Entry<K,V>> cur: positer){
			if (isInternal(cur)){
				entries.addLast(cur.element());
			}
		}
		return entries;
	}
	
	public static void main(String[] args){
		int[] myData={2,3,5,7,11,13,17,19,23,29};
		
		//test 1: LBT
		/*LinkedBinaryTree<Integer> myLBT=new LinkedBinaryTree<Integer>();
		myLBT.addRoot(myData[0]);
		System.out.println(myLBT.root().element());
		*/
		//test 2: BST
		String values1[]={"Sydney", "Beijing","Shanghai", "New York", "Tokyo", "Berlin",
				"Athens", "Paris", "London", "Cairo"}; 
		int keys1[]={20, 8, 5, 30, 22, 40, 12, 10, 3, 5};
		
		String values2[]={"Fox", "Lion", "Dog", "Sheep", "Rabbit", "Fish"}; 
		int keys2[]={40, 7, 5, 32, 20, 30};
		BinarySearchTree<Integer, String> tree1=new BinarySearchTree<Integer, String>();
		BinarySearchTree<Integer, String> tree2=new BinarySearchTree<Integer, String>();
		
		AVLTree<Integer, String> Atree1=new AVLTree<Integer, String>();
		AVLTree<Integer, String> Atree2=new AVLTree<Integer, String>();
		for(int i=0;i<keys1.length;i++){
			Atree1.insert(keys1[i], values1[i]);
		}
		for(int i=0;i<keys2.length;i++){
			Atree2.insert(keys2[i], values2[i]);
		}
		PositionList <Entry<Integer,String>> PreEntries=(PositionList<Entry<Integer, String>>) Atree1.entries();
		System.out.println(PreEntries.size());
		System.out.println("The root key of AVL1 is "+Atree1.key(Atree1.root()));
		System.out.println("The height of AVL1 is "+Atree1.height(Atree1.root()));
		for(Entry<Integer, String> e: PreEntries){
			System.out.println(e.getKey());
			System.out.println(e.getValue());
		}
		
		//PositionList <Entry<Integer,String>> InEntries=(PositionList<Entry<Integer, String>>) Atree1.inorderEntries();
		for(Entry<Integer, String> e: PreEntries){
			System.out.println(e.getKey());
			System.out.println(e.getValue());
		}
		PreEntries.first();
		
		AVLNode<Integer,String> newNode=new AVLNode<Integer,String>();
		AVLNode<Integer,String> newLeft=new AVLNode<Integer,String>();
		AVLNode<Integer,String> newRight=new AVLNode<Integer,String>();
		newNode.setLeft(newLeft);
		newNode.setRight(newRight);
		newLeft.setParent(newNode);
		newRight.setParent(newNode);
		/*AVLNode<Integer,String> newLeft=(net.datastructures.AVLTree.AVLNode<Integer,String>) newNode.getLeft();
		AVLNode<Integer,String> newRight=(net.datastructures.AVLTree.AVLNode<Integer,String>) newNode.getRight();*/
		if(newNode.getLeft()!=null){
			System.out.println("Successful initialization!");
			System.out.println(newNode.getLeft());
		}
		else{
			System.out.println("Fuck");
			System.out.println(newNode.getLeft());
		}
		
		//System.out.println("Now traversal the AVLTree!");
		//inorderTraversal(Atree1.root());
	}
}
