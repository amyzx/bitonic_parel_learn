# 双调排序，支持crypten密文排序

def compare_and_swap_joint(i, j, arr1, arr2 = None, isAsc = True):
    ''' arr1: sort by this array
        arr2: idx for arr1
        isAsc: True if ascending 
    '''
    b = (arr1[i] < arr1[j])
    smaller = b * arr1[i] + (1 - b) * arr1[j]
    larger = arr1[i] + arr1[j] - smaller

    if arr2 is not None:
        smaller2 = b * arr2[i] + (1 - b) * arr2[j]
        larger2 = arr2[i] + arr2[j] - smaller2

    if isAsc:   # ascending
        arr1[i], arr1[j] = smaller, larger
        if arr2 is not None:
            arr2[i], arr2[j] = smaller2, larger2
    else:
        arr1[i], arr1[j] = larger, smaller
        if arr2 is not None:
            arr2[i], arr2[j] = larger2, smaller2


# ============================== bitonic sort ==============================
def bitonic_sort(arr1, left, length, arr2 = None, isAsc = True):
    ''' sort arr1, arr2 is idx array
        When firstly call bitonic sort, left=0，length=len(arr1)
    '''
    if length > 1:
        m = int(length / 2)
        bitonic_sort(arr1, left, m, arr2, not isAsc)
        bitonic_sort(arr1, left + m, length - m, arr2, isAsc)
        bitonic_merge(arr1, left, length, arr2, isAsc)


def bitonic_merge(arr1, low, length, arr2 = None, isAsc = True):
    ''' assume arr1 is a bitonic sequence '''
    if length > 1:
        m = greatestPowerOfTwoLessThan(length)
        for i in range(low, low + length - m):
            compare_and_swap_joint(i, i + m, arr1, arr2, isAsc)

        bitonic_merge(arr1, low, m, arr2, isAsc)
        bitonic_merge(arr1, low + m, length - m, arr2, isAsc)
 
def greatestPowerOfTwoLessThan(n):
    ''' n may not be the power of 2 '''
    k = 1
    while (k > 0) and (k < n):
        k = k << 1
    return k >> 1
 

