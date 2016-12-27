//binary search template
class Solution{
    /**
    * nums: the integer array
    * target: number we need to find
    * return: the first position of our target
    */
    public int binarySearch(int[] nums, int target){
        if(nums == null || nums.length == 0){
            return -1;
        }

        int start = 0, end = nums.length - 1;
        //1. end condition
        while (start + 1 < end){
            //2. get middle point 
            int mid = start + (end - start) / 2;
            //3. comparation
            if(nums[mid] == target){
                end = mid;
            }
            else if(nums[mid] < target){
                start = mid;
            }
            else{
                end = mid;
            }
        }
        //break the loop: we will get nums[start,end]
        if(nums[start] == target){
            return start;
        }
        if(nums[end] == target){
            return end;
        }
        return -1;
    }

}
