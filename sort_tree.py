from directory import Folder


def sort_tree(f):
    '''(Folder) -> None
    Modify lists files in every Folder in the directory f,
    using mergesort'''

    _sort_tree(f.files, 0, len(f.files))
    for item in f.files:
        if isinstance(item, Folder):
            sort_tree(item)


# The following functions are from mergesort.py in week 9.
def _sort_tree(L, start, end):
    '''(list, int, int) -> None
    Modify list L so that L[start:end] contains the same elements,
    sorted in descending order.'''

    if end - start > 1:
        mid = (start + end) // 2
        _sort_tree(L, start, mid)
        _sort_tree(L, mid, end)
        _sort(L, start, mid, end)


def _sort(L, start, mid, end):
    '''(list, int, int, int) -> None
    Initially L[start:mid] and L[mid:end] are sorted lists.
    Modify list L to merge these sorted lists together so that
    L[start:end] is sorted in descending order according to
    the Folder's size.'''

    result = []
    i = start
    j = mid
    while i < mid and j < end:
        if L[i].size > L[j].size:
            result.append(L[i])
            i += 1
        else:
            result.append(L[j])
            j += 1
    L[start:end] = result + L[i:mid] + L[j:end]
