import tkinter as tk
from tkinter import scrolledtext, messagebox
import builtins


def parse_pcs(pcs):

    note_map = {
        "C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3, "E": 4,
        "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8, "AB": 8,
        "A": 9, "A#": 10, "BB": 10, "B": 11
    }

    if isinstance(pcs, (list, builtins.set, tuple)):
        result = builtins.set()
        for x in pcs:
            if isinstance(x, int):
                result.add(x % 12)
            elif isinstance(x, str) and x.strip().isdigit():
                result.add(int(x.strip()) % 12)
            else:
                token = str(x).strip().upper().replace('♯', '#').replace('♭', 'B')
                if token in note_map:
                    result.add(note_map[token])
        return result

    text = str(pcs)
    text = text.replace('-', ',')  
    tokens = [t.strip() for t in text.split(',') if t.strip() != '']

    result = builtins.set()
    for t in tokens:
        tok = t.upper().replace('♯', '#').replace('♭', 'B')
        if tok in note_map:
            result.add(note_map[tok])
            continue
        if tok.lstrip('-').isdigit():
            try:
                result.add(int(tok) % 12)
                continue
            except ValueError:
                pass
    return result



def generate_rotations(pcs):
    """生成集合的所有轮转排列"""
    pcs_set = parse_pcs(pcs)
    pcs_sorted = sorted(pcs_set)
    return [pcs_sorted[i:] + pcs_sorted[:i] for i in range(len(pcs_sorted))]


def inversion(pcs):
    """计算集合的倒影"""
    pcs_set = parse_pcs(pcs)
    inversion_pcs = [(12 - i) % 12 for i in pcs_set]
    return sorted(inversion_pcs)


def compacted_sets(pcs):
    """计算最紧密集合"""
    rotations = generate_rotations(pcs)
    interval_set = [(ps[-1] - ps[0]) % 12 for ps in rotations]
    min_value = min(interval_set)
    min_indices = [i for i, val in enumerate(interval_set) if val == min_value]
    return [rotations[i] for i in min_indices]


def forte_normal_form(pcs):
    """计算福特标准型"""
    set_list = compacted_sets(pcs)
    if len(set_list) == 1:
        return set_list[0]

    def recursive_selection(sets, index):
        if len(sets) == 1 or index >= len(sets[0]):
            return min(sets)
        interval_diffs = [(ps[index] - ps[0]) % 12 for ps in sets]
        min_val = min(interval_diffs)
        min_indices = [i for i, val in enumerate(interval_diffs) if val == min_val]
        return recursive_selection([sets[i] for i in min_indices], index + 1)

    return recursive_selection(set_list, 1)


def forte_prime_form(pcs):
    """计算福特基本型"""
    pcs_normal = forte_normal_form(pcs)
    inv_pcs = inversion(pcs)
    inv_normal = forte_normal_form(inv_pcs)
    sets = [pcs_normal, inv_normal]

    def recursive_selection(sets, index):
        if len(sets) == 1 or index >= len(sets[0]):
            return min(sets)
        interval_diffs = [(ps[index] - ps[0]) % 12 for ps in sets]
        min_val = min(interval_diffs)
        min_indices = [i for i, val in enumerate(interval_diffs) if val == min_val]
        return recursive_selection([sets[i] for i in min_indices], index + 1)

    temp_prime = recursive_selection(sets, 1)
    shift = temp_prime[0] % 12
    return [(i - shift) % 12 for i in temp_prime]


def subsets(pcs):
    """计算集合的所有子集"""
    pcs_set = parse_pcs(pcs)
    pcs_sorted = sorted(pcs_set)
    n = len(pcs_sorted)
    all_subsets = []
    for i in range(2 ** n):
        subset = [pcs_sorted[j] for j in range(n) if (i >> j) & 1]
        all_subsets.append(subset)
    return all_subsets


def all_transpositions(pcs):
    """生成12个移位集合（基于原始集合）"""
    pcs_set = parse_pcs(pcs)
    return [[(j + i) % 12 for j in pcs_set] for i in range(12)]


def all_inversions(pcs):
    """生成12个倒影集合（基于原始集合）"""
    inv_pcs = inversion(pcs)
    return [[(j + i) % 12 for j in inv_pcs] for i in range(12)]


def Dihedral_12_order(pcs):
    """二面体群的12阶元素"""
    return all_transpositions(pcs) + all_inversions(pcs)


def subset_class(pcs):
    """计算集合类（去重的基本型，过滤元素数<3的子集）"""
    all_subs = subsets(pcs)
    subset_classes = []
    for sub in all_subs:
        if len(sub) < 3:
            continue
        prime = forte_prime_form(sub)
        if prime not in subset_classes:
            subset_classes.append(prime)
    return subset_classes


def complementary_set(pcs):
    """计算补集"""
    universal = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
    pcs_set = parse_pcs(pcs)
    return sorted(universal - pcs_set)


def complement_set_class(pcs):
    """计算补集的基本型"""
    complement = complementary_set(pcs)
    return forte_prime_form(complement)


def find_tetrachord_genres(set1, set2):
    """计算两个三音集合合并后的四音集合及其属性"""
    set1_variants = all_transpositions(set1) + all_inversions(set1)
    set2_variants = all_transpositions(set2) + all_inversions(set2)

    four_note_sets = builtins.set()
    for v1 in set1_variants:
        for v2 in set2_variants:
            merged = sorted(builtins.set(v1) | builtins.set(v2))
            if len(merged) == 4:
                prime = tuple(forte_prime_form(merged))
                four_note_sets.add(prime)

    return [list(s) for s in four_note_sets]


def all_transpositions_with_prime_form_as_reference_frame(pcs):
    '''计算相对于集合类（基本型）的12个移位形式集合'''
    pcs_prime = forte_prime_form(pcs)  # 以基本型为参考框架
    trans_sets = []
    for i in range(12):
        T_i = [(j + i) % 12 for j in pcs_prime]
        trans_sets.append(T_i)
    return trans_sets


def all_inversions_with_prime_form_as_reference_frame(pcs):
    '''计算相对于集合类（基本型）的12个倒影形式集合'''
    pcs_prime = forte_prime_form(pcs)  # 以基本型为参考框架
    pcs_prime_inv = inversion(pcs_prime)
    inv_sets = []
    for i in range(12):
        I_i = [(j + i) % 12 for j in pcs_prime_inv]
        inv_sets.append(I_i)
    return inv_sets



def calculate():
    pcs = entry.get().strip()
    if not pcs:
        output_box.insert(tk.END, "请输入音高集合！\n\n")
        return

    try:

        inversion_result = inversion(pcs)
        rotations_result = generate_rotations(pcs)
        compacted_result = compacted_sets(pcs)
        normal_form_result = forte_normal_form(pcs)
        prime_form_result = forte_prime_form(pcs)
        subsets_result = subsets(pcs)
        subset_class_result = subset_class(pcs)

        transpositions_result = all_transpositions(pcs)
        inversions_result = all_inversions(pcs)

        prime_trans_result = all_transpositions_with_prime_form_as_reference_frame(pcs)
        prime_inv_result = all_inversions_with_prime_form_as_reference_frame(pcs)

        dihedral_result = Dihedral_12_order(pcs)
        complement_result = complementary_set(pcs)
        complement_class_result = complement_set_class(pcs)


        formatted_trans = [f"T{i}: {transpositions_result[i]}" for i in range(12)]

        formatted_inv = [f"I{i}: {inversions_result[i]}" for i in range(12)]

        formatted_prime_trans = [f"T{i}: {prime_trans_result[i]}" for i in range(12)]

        formatted_prime_inv = [f"I{i}: {prime_inv_result[i]}" for i in range(12)]

        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, f"【输入集合解析结果】: {sorted(parse_pcs(pcs))}\n\n")
        output_box.insert(tk.END, f"【倒影集合（原始集合）】: {inversion_result}\n\n")
        output_box.insert(tk.END, f"【轮转集合】:\n{rotations_result}\n\n")
        output_box.insert(tk.END, f"【最紧密轮转集合】:\n{compacted_result}\n\n")
        output_box.insert(tk.END, f"【福特标准型】: {normal_form_result}\n\n")
        output_box.insert(tk.END, f"【福特基本型】: {prime_form_result}\n\n")
        output_box.insert(tk.END, f"【所有子集】:\n{subsets_result}\n\n")
        output_box.insert(tk.END, f"【子集基本型（元素数≥3）】:\n{subset_class_result}\n\n")


        output_box.insert(tk.END, "【12个移位形式（基于原始集合）】:\n")
        for item in formatted_trans:
            output_box.insert(tk.END, f"  {item}\n")
        output_box.insert(tk.END, "\n")

        output_box.insert(tk.END, "【12个倒影形式（基于原始集合）】:\n")
        for item in formatted_inv:
            output_box.insert(tk.END, f"  {item}\n")
        output_box.insert(tk.END, "\n")

     
        output_box.insert(tk.END, "【12个移位形式（基于基本型）】:\n")
        for item in formatted_prime_trans:
            output_box.insert(tk.END, f"  {item}\n")
        output_box.insert(tk.END, "\n")

        output_box.insert(tk.END, "【12个倒影形式（基于基本型）】:\n")
        for item in formatted_prime_inv:
            output_box.insert(tk.END, f"  {item}\n")
        output_box.insert(tk.END, "\n")

    
        output_box.insert(tk.END, f"【二面体群元素】:\n{dihedral_result}\n\n")
        output_box.insert(tk.END, f"【补集】: {complement_result}\n\n")
        output_box.insert(tk.END, f"【补集的基本型】: {complement_class_result}\n\n")
        output_box.insert(tk.END, "计算完成！支持音名（如C、C#、Db）和数字，分隔符可用','或'-'\n")

    except Exception as e:
        output_box.insert(tk.END, f"计算出错: {str(e)}\n")



root = tk.Tk()
root.title("音高集合计算工具（含基本型参考框架）")
root.geometry("900x1000")  


entry_label = tk.Label(
    root,
    text="请输入音高集合（支持音名如C、C#、Db，数字0-11，分隔符用','或'-'）:",
    font=("Arial", 11)
)
entry_label.pack(pady=5)

entry = tk.Entry(root, font=("Arial", 14), width=60)
entry.pack(pady=5)
entry.bind("<Return>", lambda event: calculate()) 


calc_btn = tk.Button(
    root,
    text="开始计算",
    font=("Arial", 12),
    command=calculate,
    width=15
)
calc_btn.pack(pady=5)


output_label = tk.Label(root, text="详细计算结果:", font=("Arial", 11))
output_label.pack(pady=5)

output_box = scrolledtext.ScrolledText(
    root,
    width=100,
    height=45,
    font=("Courier", 10)  # 等宽字体保证格式对齐
)
output_box.pack(pady=5, padx=10)

root.mainloop()
