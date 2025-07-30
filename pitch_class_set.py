
#calculate all rotated sets 计算所有轮转集合
def generate_rotations(pcs):
    """生成集合的所有轮转排列"""
    pcs={int(x) for x in pcs.split(",") if x.strip().isdigit()}
    pcs_sorted = sorted(pcs)  # 先对集合进行升序排序
    return [pcs_sorted[i:] + pcs_sorted[:i] for i in range(len(pcs_sorted))]

#calculate inversional sets 计算倒影
def inversion(pcs):
    pcs = {int(x) for x in pcs.split(",") if x.strip().isdigit()}
    pcs_sorted = sorted(pcs)  # 先对集合进行升序排序
    inversion_pcs=[]
    for i in pcs:
        pitch_class=(12-i) % 12
        inversion_pcs.append(pitch_class)
    inversion_pcs=sorted(inversion_pcs)
    return inversion_pcs

#calculate compacted sets 计算最紧密集合
def compacted_sets(pcs):
    rotations = generate_rotations(pcs)  # generate all rotated sets 生成所有轮转排列
    interval_set = [] 
    # calculate width of rotated sets轮转排列的宽度
    for ps in rotations:
        interval = (ps[-1] - ps[0]) % 12
        interval_set.append(interval)
    # 找到最小值及其索引
    min_value = min(interval_set)  # 获取最小宽度
    min_indices = [index for index, value in enumerate(interval_set) if value == min_value]  # 获取最小值的索引
    #compacted sets
    compacted_sets=[]
    for i in min_indices:
        compacted_sets.append(rotations[i])
    return compacted_sets

#normal form 计算标准型
def forte_normal_form(pcs):
    set_list = compacted_sets(pcs)  # 获取最窄集合
    if len(set_list) == 1:
        return set_list[0]  # 如果只有一个最窄集合，则直接输出
    def recursive_selection(sets, index):
        #如果最窄集合只有一个，那么直接输出就是福特标准型
        if len(sets) == 1 or index >= len(sets[0]):
            return min(sets)  # 若最终仍有多个集合，则选取最左侧最小者
        #开始计算
        interval_diffs = []
        for ps in sets:
            interval = (ps[index] - ps[0]) % 12  # 计算第2, 3, ..., index个音与第1个音在12模下的音程
            interval_diffs.append(interval)
        min_value = min(interval_diffs)  # 获取最小音程
        min_indices = [i for i, value in enumerate(interval_diffs) if value == min_value]  # 获取最小值索引
        filtered_sets = [sets[i] for i in min_indices]  # 获取符合条件的集合
        return recursive_selection(filtered_sets, index + 1)  
    forte_normal_form = recursive_selection(set_list, 1)  # 计算最终福特标准型
    return forte_normal_form

#计算基本型
def forte_prime_form(pcs):
    pcs_normal_form = forte_normal_form(pcs)  # 原位集合标准型
    inversion_pcs = inversion(pcs)  # 倒影集合
    inversion_pcs_normal_form = forte_normal_form(",".join(map(str, inversion_pcs)))  # 转换为字符串格式后传入

    sets = [pcs_normal_form, inversion_pcs_normal_form]  # 创建包含两个集合的列表

    def recursive_selection(sets, index):
        """递归计算福特标准型"""
        if len(sets) == 1 or index >= len(sets[0]):
            return min(sets)  # 选取最左侧最小者

        interval_diffs = [(ps[index] - ps[0]) % 12 for ps in sets]  # 计算第 index 个音相对于第一个音的音程
        min_value = min(interval_diffs)  # 获取最小音程
        min_indices = [i for i, value in enumerate(interval_diffs) if value == min_value]  # 获取最小值索引
        filtered_sets = [sets[i] for i in min_indices]  # 选出符合条件的集合

        return recursive_selection(filtered_sets, index + 1)  # 递归进行下一步计算
    forte_prime_form_temp = recursive_selection(sets, 1)  # 计算最终福特标准型
    a=(forte_prime_form_temp[0]-0)%12
    forte_prime_form=[(i-a)%12 for i in forte_prime_form_temp]#左侧为0
    return forte_prime_form

#计算子集
def subsets(pcs):
    """计算集合的所有子集，确保每个子集的元素都是整数"""
    pcs = {int(x) for x in pcs.split(",") if x.strip().isdigit()}  # 转换为整数集合
    pcs_sorted = sorted(pcs)  # 先对集合进行升序排序
    n = len(pcs_sorted)
    all_subsets = []
    for i in range(2 ** n):  # 2^n 次循环，枚举所有子集
        subset = []
        for j in range(n):  # 遍历列表的每个元素
            if (i >> j) & 1:  # 检查 i 的二进制表示中第 j 位是否为 1
                subset.append(pcs_sorted[j])  # 使用列表索引访问
        all_subsets.append(subset)
    return all_subsets

#12个移位集合
def all_transpositions(pcs):
    pcs = {int(x) for x in pcs.split(",") if x.strip().isdigit()}
    pcs_sorted = sorted(pcs)  # 先对集合进行升序排序
    transoposion_sets=[]
    for i in range(0,12):
        T_i=[]
        for j in pcs:
            j=(j+i)%12
            T_i.append(j)
        transoposion_sets.append(T_i)
    return transoposion_sets

#12个倒影集合
def all_inversions(pcs):
    pcs=inversion(pcs)
    inversion_sets=[]
    for i in range(0, 12):
        I_i = []
        for j in pcs:
            j = (j + i) % 12
            I_i.append(j)
        inversion_sets.append(I_i)
    return inversion_sets

def Dihedral_12_order(pcs):
    Dihedral_12 = all_transpositions(pcs) + all_inversions(pcs)
    return Dihedral_12


def subset_class(pcs):
    all_subsets = subsets(pcs)  # 生成所有子集
    subset_class = []  # 用列表存储，确保不会覆盖 set 关键字

    for i in all_subsets:
        if len(i) < 3:  # 过滤掉空集和单元素集
            continue
        prime_form = forte_prime_form(",".join(map(str, i)))  # 计算基本型
        if prime_form not in subset_class:  # 避免重复
            subset_class.append(prime_form)

    return subset_class  # 直接返回列表


def complementary_set(pcs):
    """计算集合 pcs 关于全集 [0,1,2,...,11] 的补集，并返回补集及其基本型"""
    universal_set = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}  # 避免 set() 可能被覆盖的问题
    pcs = {int(x) for x in pcs.split(",") if x.strip().isdigit()}  # 转换为整数集合
    complement = sorted(universal_set - pcs)  # 计算补集并排序
    return complement  # 返回补集及其基本型

def complement_set_class(pcs):
    complement=complementary_set(pcs)
    # 将列表转换为符合 forte_prime_form() 输入格式的字符串
    complement_str = ",".join(map(str, complement))
    # 计算补集的福特基本型
    complement_set_class = forte_prime_form(complement_str)
    return complement_set_class


def find_tetrachord_genres(set1, set2):
    """计算两个三音集合的 24 种变换，筛选所有四音集合，并计算其 Forte Prime Form，同时分析补集及其子集"""
    print("集合1的Prime Form", forte_prime_form(set1))
    print("集合2的Prime Form", forte_prime_form(set2))

    set1_variants = all_transpositions(set1) + all_inversions(set1)
    set2_variants = all_transpositions(set2) + all_inversions(set2)

    merged_sets = []
    four_note_sets = set()

    for variant1 in set1_variants:
        for variant2 in set2_variants:
            merged_set = sorted(set(variant1) | set(variant2))
            merged_sets.append(merged_set)

            if len(merged_set) == 4:
                forte_form = tuple(forte_prime_form(",".join(map(str, merged_set))))
                four_note_sets.add(forte_form)

    print("包含两个三音集合的四音集合Prime Form：", [list(s) for s in four_note_sets])

    four_note_complements = []
    valid_complements = []
    valid_complement_classes = []

    set1_prime = forte_prime_form(set1)
    set2_prime = forte_prime_form(set2)

    for s in four_note_sets:
        complement = complementary_set(",".join(map(str, s)))
        if complement:
            four_note_complements.append(complement)

            complement_subsets = subset_class(",".join(map(str, complement)))

            for subset in complement_subsets:
                if set1_prime in subset_class(",".join(map(str, subset))) and set2_prime in subset_class(
                        ",".join(map(str, subset))):
                    valid_complements.append(complement)
                    complement_class = forte_prime_form(",".join(map(str, complement)))
                    valid_complement_classes.append(complement_class)
                    break

    print("所有四音集合的补集：", four_note_complements)
    print("四音集合的补集：", valid_complements)
    print("补集的Prime Form：", valid_complement_classes)

    return ([list(s) for s in four_note_sets], four_note_complements, valid_complements, valid_complement_classes)


def find_one_more_pitch_pcs(pcs):
    """对输入的集合进行扩展分析，计算添加一个音后的 Forte Prime Form，并检查补集的子集类"""

    pcs_set = {int(x) for x in pcs.split(",") if x.strip().isdigit()}  # 转换为整数集合
    existing_prime_form = forte_prime_form(pcs)  # 原集合的 Forte Prime Form

    print(f"原集合: {sorted(pcs_set)}")
    print(f"原集合的 Forte Prime Form: {existing_prime_form}\n")

    final_results = []  # 存储符合条件的扩展集合及其补集

    # 遍历 0-11，尝试添加一个新的音
    for new_pitch in range(12):
        if new_pitch not in pcs_set:  # 不能与已有音重复
            new_set = sorted(pcs_set | {new_pitch})  # 生成新的集合

            # 计算新集合的 Forte Prime Form
            prime_form = forte_prime_form(",".join(map(str, new_set)))

            # 计算补集的 Forte Prime Form
            complement = complementary_set(",".join(map(str, new_set)))
            complement_prime = forte_prime_form(",".join(map(str, complement)))

            # 计算补集的子集类
            complement_subsets = subset_class(",".join(map(str, complement)))

            # **检查补集的子集类是否包含原集合的 Forte Prime Form**
            if existing_prime_form in complement_subsets:
                final_results.append((new_set, complement))  # 同时存储扩展集合和补集

    # **最终输出**
    print("\n【符合条件的扩展集合 & 其补集】")
    for new_set, complement in final_results:
        print(f"扩展集合: {new_set}  -> 补集: {complement}")

    return final_results  # 返回所有符合条件的扩展集合及补集


pcs=input("请输入一个无序集合（英文逗号分隔）：")
numbers = {int(x) for x in pcs.split(",") if x.strip().isdigit()}
#集合升序排列
sorted_numbers = sorted(numbers)
print("集合:", sorted_numbers)
set=pcs
# print("倒影集合：",inversion(pcs))
# print("轮转集合为：",generate_rotations(pcs))
# print("最紧密集合为：",compacted_sets(pcs))
# print("福特norm form为：",forte_normal_form(pcs))
# print("福特prime form型为：",forte_prime_form(pcs))
# print("所有子集：",subsets(pcs))
# print("12个移位集合：",all_transpositions(pcs))
# print("12个倒影集合：",all_inversions(pcs))
# print("二面体群：",Dihedral_12_order(pcs))
# print("所有子集类(去除空集、单音集、二音集）：",subset_class(pcs))
# print("补集为：",complementary_set(pcs))
# print("补集类为：",complement_set_class(pcs))
print("拓展后的集合与补集为：",find_one_more_pitch_pcs(pcs))
