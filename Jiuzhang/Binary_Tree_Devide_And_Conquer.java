DFS:
    Preorder/Inorder/Postorder Traversal
    Devide and Conquer
    Non-recursion VS Traverse
BFS: iterative
Operations of BST: Insert / Remove / Find / Validate

//1. Preorder
//1.1 Traverse
public class Solution{
    public ArrayList<Integer> preorderTraversal(TreeNode root){
        ArrayList<Integer> result = new ArrayList<Integer>();
        traverse(root, result);
        return result;
    }
    private void traverse(TreeNode root, ArrayList<Integer> result){
        if(root == null){
            return;
        }
        result.add(root.val);
        traverse(root.left,result);
        traverse(root.right,result);
    }
} 
//1.2 Devide and Conquer: 
public class Solution{
    public ArrayList<Integer> preorderTraversal(TreeNode root){
        ArrayList<Integer> result = new ArrayList<Integer>();
        // null or leaf
        if(root == null){
            return result;
        }
        //devide
        ArrayList<Integer> left = preorderTraversal(root.left);
        ArrayList<Integer> right = preorderTraversal(root.right);
        //conquer
        result.add(root.val);
        result.addAll(left);
        result.addAll(right);
        return result;
    }
}
//1.3 non-recursive: stack --> recommend
public class Solution{
    public ArrayList<Integer> preorderTraversal(TreeNode root){
        Stack<TreeNode> stack = new Stack<TreeNode>();
        List<Integer> preorder = new ArrayList<Integer>();
        if(root == null){
            return preorder;
        }
        stack.push(root);
        while(!stack.isEmpty()){
            TreeNode node = stack.pop();
            preorder.add(node.val);
            if(node.right != null){
                stack.push(node.right);
            }
            if(node.left != null){
                stack.push(node.left);
            }
        }
        return preorder;
    }
}

///////////////////////////////////////
//2. Maximum depth
//2.1 traversal
public class Solution{
    private int depth;
    public int maxDepth(TreeNode root){
        depth = 0;
        helper(root, 1);
        return depth;
    }
    private void helper(TreeNode currNode , int currDepth){
        if(currNode == null){
            return; //depth = 0
        }
        if(currDepth > depth){
            depth = currDepth;
        }
        helper(currNode.left, currDepth + 1);
        helper(currNode.right, currDepth + 1);
    }
}
//2.2 devide and conquer
public class Solution{
    public int maxDepth(TreeNode root){
        if(root = null){
            return 0;
        }
        int left = maxDepth(root.left);
        int right = maxDepth(root.right);
        return Math.max(left,right)+1;
    }
}

///////////////////////////////////////
//3. Balanced BST
//3.1 without result type
public class Solution{
    public boolean isBalanced(TreeNode root){
        return maxDepth(root) != -1;
    }
    //return the maxDepth, if not balanced --> return -1
    private int maxDepth(TreeNode root){
        if(root = null){
            return 0;
        }
        int left = maxDepth(root.left);
        int right = maxDepth(root.right);
        //check
        if(left == -1 || right == -1 || Math.abs(left-right) > 1){
            return -1;
        }
        return Math.max(left,right)+1;
    }
}
//3.2 General format: create new result type
class ResultType{
    public boolean isBalanced;
    public int maxDepth;
    public ResultType(boolean isBalanced, int maxDepth){
        this.isBalanced = isBalanced;
        this.maxDepth = maxDepth;
    }
}
public class Solution{
    public boolean isBalanced(TreeNode root){
        return helper(root).isBalanced;
    }
    private ResultType helper(TreeNode root){
        if(root == null){
            return new ResultType(true, 0);
        }
        ResultType left = helper(root.left);
        ResultType left = helper(root.right);
        //subtree not balance
        if(!left.isBalanced || !right.isBalanced){
            return new ResultType(false, -1);
        }
        //root not balance
        if(Math.abs(left.maxDepth-right.maxDepth) > 1){
            return new ResultType(false, -1);
        }
        return new ResultType(true, Math.max(left.maxDepth, right.maxDepth) + 1);
    }
}

///////////////////////////////////////
//4. Lowest Common Ancestor
public class Solution{
    /* 
    * left & right != null --> root is LCA
    * left || right != null --> in one subtree
    * all null --> null
    */
    public TreeNode lowestCommonAncestor(TreeNode root,
                                    TreeNode A,
                                    TreeNode B){
        if(root == null || root == A || root == B){
            return root;
        }
        TreeNode left = lowestCommonAncestor(root.left, A, B);
        TreeNode right = lowestCommonAncestor(root.right, A, B);
        if(left != null && right != null){
            return root;
        }
        if(left != null){
            return left;
        }
        if(right != null){
            return right;
        }
        return null;
    }
}
///////////////////////////////////////
//5. Maximum Path Sum: 
//5.1 the max sum of values in path: from root to any node
public int maxPathSum(TreeNode root){
    if(root == null){
        return 0;
    }
    //divide
    int left = maxPathSum(root.left);
    int right = maxPathSum(root.right);
    //conquer
    //if left&right < 0 , we do not need to add
    return Math.max(Math.max(left,right),0)+root.val;
}
//5.2 viaration: start from any node
//all-left || all-right || from left to right
// max left subpath(may be 0) + root + max right path(may be 0)
public class Solution{
    private class ResultType{
        // singlePath: max path from root, can have no node
        // maxPath: any node to any node, at least 1 node
        int singlePath, maxPath;
        ResultType(int singlePath, int maxPath){
            this.singlePath = singlePath;
            this.maxPath = maxPath;
        }
    }

    private ResultType helper(TreeNode root){
        if(root == null){
            return new ResultType(0, Integer.MIN_VALUE);
        }
        //Divide
        ResultType left = helper(root.left);
        ResultType right = helper(root.right);
        //Conquer
        //compute new single path
        int singlePath =Math.max(Math.max(left.singlePath, right.singlePath) + root.val, 0);
        //compute new max path
        int maxPath = Math.max(left.maxPath, right.maxPath);
        maxPath = Math.max(maxPath, left.singlePath + right.singlePath + root.val);

        return new ResultType(singlePath, maxPath);
    }

    public int maxPathSum(TreeNode root){
        ResultType result = helper(root);
        return result.maxPath; 
    }
}
///////////////////////////////////////
//6. BFS Traversal
//6.1 2 queues
[A] [B,C], [F,null, D,E]
Q1.enqueue(A) //[A]
Q1.dequeue(), Q2.enqueue(B), Q2.enqueue(C) //[B,C]
Q2.dequeue(), Q1.enqueue(F), Q2.dequeue(), Q1.enqueue(D,E) //[F,D,E]

public ArrayList<ArrayList<Integer>> levelOrder(TreeNode root){
    ArrayList result = new ArrayList();

    if(root == null){
        return result;
    }
    ArrayList<TreeNode> Q1 = new ArrayList<TreeNode>();
    ArrayList<TreeNode> Q2 = new ArrayList<TreeNode>();
    Q1.add(root);
    while(Q1.size() != 0){
        ArrayList<Integer> level = new ArrayList<Integer>();
        Q2.clear();
        for(int i = 0; i < Q1.size() ; i++){
            TreeNode node = Q1.get(i);
            level.add(node.val);
            if(node.left != null){
                Q2.add(node.left);
            }
            if(node.right != null){
                Q2.add(node.right);
            }
        }
        //swap Q1 and Q2
        ArrayList<TreeNode> temp = Q1;
        Q1 = Q2;
        Q2 = temp;

        result.add(level);
    }
    return result;
}

//6.2 1 queue + 1 dummy node

//6.3 1 queue : best
public ArrayList<ArrayList<Integer>> levelOrder(TreeNode root){
    ArrayList result = new ArrayList();

    if(root == null){
        return result;
    }

    Queue<TreeNode> queue = new LinkedList<TreeNode>();
    queue.offer(root);

    while(!queue.isEmpty()){
        ArrayList<Integer> level = new ArrayList<Integer>();
        int size = queue.size();
        for(int i = 0; i < size ; i++){
            TreeNode head = queue.poll();
            level.add(head.val);
            if(head.left != null){
                queue.offer(head.left);
            }
            if(head.right != null){
                queue.offer(head.right);
            }
        }
        result.add(level);
    }
    return result;
}

///////////////////////////////////////
//7. Validate BST
//7.1 inorder, then validate
/** 7.2 Divide and conquer
* find the largest node in left subtree
* find the smallest node in right subtree
* 
*/
class ResultType{
    boolean isBST;
    int maxValue, minValue;
    ResultType(boolean isBST, int maxValue, int minValue){
        this.isBST = isBST;
        this.maxValue = maxValue;
        this.minValue = minValue;
    }
}
public boolean isValidBST(TreeNode root){
    ResultType result = validateHelper(root);
    return result.isBST;
}

private ResultType validateHelper(TreeNode root){
    if(root == null){
        return new ResultType(true, Integer.MIN_VALUE, Integer.MAX_VALUE);
    }
    ResultType left = validateHelper(root.left);
    ResultType right = validateHelper(root.right);
    if(!left.isBST || !right.isBST){
        return new ResultType(false, 0, 0);
    }
    if(root.left != null && left.maxValue >= root.val || root.right != null && right.minValue <= root.val){
        return new ResultType(false, 0, 0);
    }

    return new ResultType(true, Math.max(root.val, right.maxValue), Math.min(root.val, left.minValue));
}
//////same method
public class Solution {
    public boolean isValidBST(TreeNode root) {
        return helper(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    
    public boolean helper(TreeNode root, long minVal, long maxVal) {
        if (root == null) return true;
        if (root.val >= maxVal || root.val <= minVal) return false;
        return helper(root.left, minVal, root.val) && helper(root.right, root.val, maxVal);
    }
}
///////////////////////////////////////
//8. BST Iterator(hard)

public class BSTIterator{
    private Stack<TreeNode> stack = new Stack<>();
    private TreeNode curr;

    public BSTIterator(TreeNode root){
        curr = root;
    }

    public boolean hasNext(){
        return (curr != null || !stack.isEmpty());
    }

    public TreeNode next(){
        while(curr != null){
            stack.push(curr);
            curr = curr.left;
        }
        curr = stack.pop();
        TreeNode result = curr;
        curr = curr.right;

        return result
    }
}
