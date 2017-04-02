% Test Cases for COMP9414 Assignment 1
% Yunqiu Xu

% Question 1
weird_sum([], R). % 0
weird_sum([3,6,2,-1], R). % R = 33
weird_sum([0,1,2,3,4,5,-6], R). % 5*5 - 0 - 1 - 2 - 6 = 16
weird_sum([0,-1,-2,-3,-4,-5,-6], R). % -21
weird_sum([0,0,1,1,2,2,4,4,6,-6], R). % 6 * 6 - 0 - 0 - 1 - 1 - 2 - 2 - 6 = 24
weird_sum([1,3,5,7,9,10,8,6,4,2,2,2,2,2,2], R). % 5^2 + 6^2 + 7^2 + 8^2 + 9^2 + 10^2 - 1 - 2 - 2 - 2 - 2 - 2 - 2 = 342
weird_sum([-1,3,-5,7,-9,9], R). % 7^2 + 9^2 -1 - 5 - 9

% Question 2
parent(albert,georges).
parent(berenice, georges).
parent(albert,isidore).
parent(berenice,isidore).
parent(charles,henriette).
parent(darlene,henriette).
parent(charles,josephine).
parent(darlene,josephine).
parent(charles,katarina).
parent(darlene,katarina).
parent(etienne, louis).
parent(floriane, louis).
parent(georges,maurice).
parent(henriette, maurice).
parent(georges, noemie).
parent(henriette, noemie).
parent(isidore,ophelie).
parent(josephine, ophelie).
parent(isidore, patrick).
parent(josephine, patrick).
parent(isidore, quentin).
parent(josephine, quentin).
parent(katarina, rosalie).
parent(louis, rosalie).
parent(katarina, stephanie).
parent(louis, stephanie).

male(albert).
male(charles).
male(georges).
male(isidore).
male(etienne).
male(louis).
male(maurice).
male(patrick).
male(quentin).

female(berenice).
female(darlene).
female(henriette).
female(josephine).
female(katarina).
female(floriane).
female(noemie).
female(ophelie).
female(rosalie).
female(stephanie).


same_name(albert, berenice). % false
same_name(albert, georges). % true
same_name(berenice, isidore). %false
same_name(isidore, albert). %true
same_name(georges, isidore). %true
same_name(isidore, georges). %true
same_name(charles, henriette). %true
same_name(katarina, darlene). %false
same_name(katarina, josephine). %true
same_name(josephine, henriette). %true
same_name(georges, henriette). %false
same_name(louis, floriane). %false
same_name(louis, etienne). %true
same_name(maurice, patrick). %true
same_name(noemie, maurice). %true
same_name(ophelie, quentin). %true
same_name(rosalie, stephanie). %true
same_name(quentin, stephanie). %false
same_name(rosalie, noemie). %false
same_name(berenice, noemie). %false
same_name(albert, quentin). %true

same_name(noemie, X). %[maurice, noemie, georges,isidore, ophelie, patrick, quentin, albert]
same_name(X, henriette). %[henriette, josephine, katarina, charles]
same_name(louis, X). %[etienne, louis, rosalie, stephanie]
same_name(albert, X). %[maurice, noemie, georges,isidore, ophelie, patrick, quentin, albert]
same_name(X, darlene). %none

% Question 3
log_table([1,3.7,5], Result). % Result = [[1, 0.0], [3.7, 1.308332819650179], [5, 1.6094379124341003]].
log_table([1,2,3,4,5], Result).
log_table([64],Result).
log_table([100000000,2], Result).

% Question 4
paruns([], R).
paruns([8,0,4,3,7,2,-1,9,9], R).
paruns([-1,-2,-2,-3,3,-3,4,-4,-4,4,-5,5,-5,5,6,-5], R).
paruns([8,0,4,3,7,2,-1,9,9,6,8,0,2,-1,7,8,0,1,1,2], R).

% Question 5
is_heap(tree(empty,5,empty)). % true
is_heap(tree(tree(tree(empty,4,empty),3,tree(empty,5,empty)),6,tree(tree(empty,9,empty),7,empty))). % false
is_heap(tree(empty,3,tree(tree(empty,8,empty),5,tree(empty,7,empty)))). % true 
is_heap(tree(tree(tree(empty,1,empty),1,tree(empty,1,empty)),1,tree(tree(empty,1,empty),1,empty))). % true
