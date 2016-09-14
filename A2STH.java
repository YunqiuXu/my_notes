//1. Do we need to implement a mergesort fun?
I do not think so , this is just the "merge" part of merge sort
because the 2 sublists are all sorted.
I implement the merge process in the Q2 main function 

https://github.com/aistrate/AlgorithmsSedgewick/blob/master/2-Sorting/2-2-Mergesort/Merge.java
line 21-45 can be a good ref

//2. Do u use comparable
Y, I import it and create a DefaultComparator object

//3. do we need a func to create a BST from the sorted list
Y, and you can find similar code online
By finding the middle position and ... blablabla
You need to use recursion, this can be performed in O(n)

//4. For cloning , is it in preorder
Y, similar
Clone the current node, 
Perform cloning on its left subtree recursively
Perform cloning on ite right subtree recursively

//5. is it correct to add to a list
I think it is right but i have not tested my code

//6. r u using avlnodes somewhere
Y, actually I use AVLNode as possible as i can
the type of elements in your positionlist should be Position<Entry<K, V>>
Then when i build the new tree I change them to BTPosition<Entry<K,V>>
Finally I create AVLNode<Entry<K,V>> to store them
This can be ok and I do not need to add cast

//7. I do not understand what u mean in Q7
