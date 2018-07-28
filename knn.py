'''
1. which dimension do we split along?
2. which value do we split at?
3. when do we stop

'''
import math
from itertools import product


class Node(object):
    left = None
    right = None
    is_leaf = False
    leaf_data = None
    split_value = None
    tight_bound = None

    def __str__(self):
        return "left: {}\nright: {}\nsplit_value: {}\nis leaf: {}\nleaf_data{}".\
            format(self.left, self.right, self.split_value, self.is_leaf, self.leaf_data)

def creat_leaf(data):
    node = Node()
    node.is_leaf = True
    node.leaf_data = data
    node.tight_bound = get_tight_bound(data)
    return node


def get_split_value(feat):
    v = (max(feat) + min(feat)) / 2   # mid-point
    return v


def create_kd_tree(data, split_at_dim=0):
    # root
    node = Node()

    # stop
    if len(data) <= 2:  # 2 data points in a node
        return creat_leaf(data)

    # split value
    split_at_dim = split_at_dim % 2 # 2 features
    feats = list(zip(*data))
    feat = feats[split_at_dim]
    split_value = get_split_value(feat)

    # left, right data
    left_data_ids = []
    right_data_ids = []
    for i, elem in enumerate(feat):
        if elem < split_value:
            left_data_ids.append(i)
        else:
            right_data_ids.append(i)

    left_data = [data[i] for i in left_data_ids]
    right_data = [data[i] for i in right_data_ids]

    # recursive
    left_node = create_kd_tree(left_data, split_at_dim + 1)
    right_node = create_kd_tree(right_data, split_at_dim + 1)

    node.left = left_node
    node.right = right_node
    node.split_value = split_value
    return node

def get_tight_bound(data):
    feat_mins = list(map(min, zip(*data)))
    feat_maxs = list(map(max, zip(*data)))

    return feat_mins, feat_maxs


def within_class_dist(tree, query, current_dim=0):
    if tree.is_leaf == True:
        min_point, min_value = get_min_dist(tree.leaf_data, query)
        return min_point, min_value

    current_dim = current_dim % 2 # 2 is no. of features
    split_value = tree.split_value
    point_value = query[current_dim]

    if point_value < split_value:
        return within_class_dist(tree.left, query, current_dim + 1)
    else:
        return within_class_dist(tree.right, query, current_dim + 1)


def dfs_traverse(tree, query):
    global min_dist
    global min_point

    if tree.is_leaf == True:
        # prune
        bounds = list(product(*tree.tight_bound))
        _, dist_to_area = get_min_dist(bounds, query)
        if dist_to_area > min_dist:
            print("This node get pruned")

        # get dist
        tmp_point, tmp_dist = get_min_dist(tree.leaf_data, query)
        if tmp_dist < min_dist:
            min_dist = tmp_dist
            min_point = tmp_point

    else:
        dfs_traverse(tree.left, query)
        dfs_traverse(tree.right, query)


def get_min_dist(data, query):
    def dist_func(p1, p2):
        assert len(p1) == len(p2)

        # Euclidean dist
        square_sum = sum([(p1[i] - p2[i]) ** 2 for i in range(len(p1))])
        dist = math.sqrt(square_sum)

        return dist

    dists = [dist_func(query, p) for p in data]
    id, value = min(enumerate(dists), key=lambda x: x[1])

    return data[id], value




if __name__ == "__main__":
    X = [(0.59, 0.9), (0.89, 0.82), (0.04, 0.69), (0.38, 0.52), (0.66, 0.19), (0.27, 0.72), (0.8, 0.6)]
    query_point = (0.5, 0.66)
    tree = create_kd_tree(X)
    min_point, min_dist = within_class_dist(tree, query_point)
    dfs_traverse(tree, query_point)
    print("data point:", min_point, "dist:", min_dist)

