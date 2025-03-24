import tkinter as tk
from tkinter import scrolledtext



#计算所有轮转集合
def generate_rotations(pcs):
    """生成集合的所有轮转排列"""
    pcs={int(x) for x in pcs.split(",") if x.strip().isdigit()}
    pcs_sorted = sorted(pcs)  # 先对集合进行升序排序
    return [pcs_sorted[i:] + pcs_sorted[:i] for i in range(len(pcs_sorted))]

#计算倒影
def inversion(pcs):
    pcs = {int(x) for x in pcs.split(",") if x.strip().isdigit()}
    pcs_sorted = sorted(pcs)  # 先对集合进行升序排序
    inversion_pcs=[]
    for i in pcs:
        pitch_class=(12-i) % 12
        inversion_pcs.append(pitch_class)
    inversion_pcs=sorted(inversion_pcs)
    return inversion_pcs

#计算最紧密集合
def compacted_sets(pcs):
    rotations = generate_rotations(pcs)  # 生成所有轮转排列
    interval_set = []  # 存储所有轮转排列的宽度
    # 计算每个轮转排列的宽度
    for ps in rotations:
        interval = (ps[-1] - ps[0]) % 12
        interval_set.append(interval)
    # 找到最小值及其索引
    min_value = min(interval_set)  # 获取最小宽度
    min_indices = [index for index, value in enumerate(interval_set) if value == min_value]  # 获取最小值的索引
    #输出最窄集合
    compacted_sets=[]
    for i in min_indices:
        compacted_sets.append(rotations[i])
    return compacted_sets

#计算标准型
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
        return recursive_selection(filtered_sets, index + 1)  # 递归继续计算下一个音程
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

    pitch_set = {int(x) for x in pcs.split(",") if x.strip().isdigit()}
    existing_prime_form = forte_prime_form(pcs)

    output_log = []
    output_log.append(f"原集合: {sorted(pitch_set)}")
    output_log.append(f"原集合的 Forte Prime Form: {existing_prime_form}\n")

    expanded_pitch_sets = []
    expanded_prime_forms = set()
    complement_prime_forms = set()
    final_results = []
    unique_final_results = set()

    for new_pitch in range(12):
        if new_pitch not in pitch_set:
            new_pitch_set = sorted(pitch_set | {new_pitch})
            expanded_pitch_sets.append(new_pitch_set)

            prime_form = tuple(forte_prime_form(",".join(map(str, new_pitch_set))))
            expanded_prime_forms.add(prime_form)

            complement = complementary_set(",".join(map(str, new_pitch_set)))
            complement_prime = tuple(forte_prime_form(",".join(map(str, complement))))
            complement_prime_forms.add(complement_prime)

            complement_subsets = subset_class(",".join(map(str, complement)))

            if existing_prime_form in complement_subsets:
                final_results.append((tuple(new_pitch_set), prime_form, tuple(complement), complement_prime))
                unique_final_results.add((prime_form, complement_prime))

    # **输出所有拓展后的集合（未计算 Prime Form）**
    output_log.append("\n所有附加一个音后的集合（未计算 Prime Form）")
    for new_pitch_set in expanded_pitch_sets:
        output_log.append(f"附加一个音后的集合: {new_pitch_set}")

    # **输出所有拓展后的集合（去重）**
    output_log.append("\n所有附加一个音后的集合")
    for prime_form in sorted(expanded_prime_forms):
        output_log.append(f"附加一个音后集合的 Prime Form: {list(prime_form)}")

    # **输出所有扩展集合的补集（去重）**
    output_log.append("\n所有附加一个音后的集合的补集")
    for prime_form in sorted(complement_prime_forms):
        output_log.append(f"补集的 Prime Form: {list(prime_form)}")

    # **最终去重后输出符合条件的扩展集合及其补集**
    output_log.append("\n符合条件的附加一个音后集合 & 其补集（最终去重）")
    final_results_filtered = []
    for prime_form, complement_prime in sorted(unique_final_results):
        for new_pitch_set, p_form, complement, c_prime in final_results:
            if p_form == prime_form and c_prime == complement_prime:
                final_results_filtered.append((new_pitch_set, prime_form, complement, complement_prime))
                break

    if not final_results_filtered:
        output_log.append("没有符合条件的附加音集合！")
    else:
        for new_pitch_set, prime_form, complement, complement_prime in final_results_filtered:
            output_log.append(f"集合: {list(new_pitch_set)} -> Prime Form: {list(prime_form)} | "
                              f"补集: {list(complement)} -> Prime Form: {list(complement_prime)}\n")

    # **返回所有计算步骤**
    return output_log, expanded_pitch_sets, expanded_prime_forms, complement_prime_forms, final_results_filtered

# **GUI 版本**
def find_one_more_pitch_pcs_gui():
    """GUI 版本的 find_one_more_pitch_pcs"""
    pcs = entry.get()
    output_box.delete(1.0, tk.END)

    if not pcs:
        output_box.insert(tk.END, "请输入一个无序集合（用逗号分隔）！\n")
        return

    try:
        output_log, expanded_pitch_sets, expanded_prime_forms, complement_prime_forms, final_results_filtered = find_one_more_pitch_pcs(pcs)

        for line in output_log:
            output_box.insert(tk.END, line + "\n")

    except Exception as e:
        output_box.insert(tk.END, f"发生错误：{e}\n")

# **创建 GUI 界面**
root = tk.Tk()
root.title("果粒与喜鹊与鱼")
root.geometry("900x800")

# **输入框**
entry_label = tk.Label(root, text="请输入一个无序集合（逗号分隔）：")
entry_label.pack()

entry = tk.Entry(root, width=50)
entry.pack()
entry.bind("<Return>", lambda event: find_one_more_pitch_pcs_gui())

# **计算按钮**
calculate_button = tk.Button(root, text="计算", command=find_one_more_pitch_pcs_gui)
calculate_button.pack()

# **滚动文本框用于显示输出**
output_box = scrolledtext.ScrolledText(root, width=220, height=100)
output_box.pack()

# **运行 GUI**
root.mainloop()