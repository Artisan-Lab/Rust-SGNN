'''
特殊符号
*       (star_token: Star
         op: Deref(Star,),)
&       (and_token: And,)
<>      ( lt_token: Lt,  gt_token: Gt,)
::      ( Colon2,
          colon2_token: Colon2,)
[]      (bracket_token: Bracket,)
..      (limits: HalfOpen(Dot2,),)

'''

import re
import os

# 指定目录路径
dir_path = '/home/rose/code/ast/1'
# 遍历目录下的所有文件
for input_file in os.listdir(dir_path):
    var_dict = {}
    # 判断是否为文本文件
    res_dict = {
        "Box": None,
        "MaybeUninit": None,
        "Arc": None,
        "Vec": None,
        "slice": None,
        "vec!": None,
        "String": None,
        "struct": None,
        "UnsafeCell": None,
        "Option": None,
        "Result": None,
        "Some": None,
        "NonZero": None,
        "NonNull": None,
        "mut": None,
        "const": None,
        "array_assume_init": None,
        "as_bytes_mut": None,
        "as_chunks_unchecked": None,
        "as_chunks_unchecked_mut": None,
        "as_ptr": None,
        "as_mut_ptr": None,
        "as_ref": None,
        "as_uninit_ref": None,
        "assume_init": None,
        "as_mut": None,
        "clone": None,
        "dealloc": None,
        "deallocate": None,
        "drop": None,
        "drop_in_place": None,
        "downcast_unchecked": None,
        "expect": None,
        "forget": None,
        "free": None,
        "from_le_bytes": None,
        "from_raw": None,
        "from_raw_in": None,
        "from_raw_parts": None,
        "from_raw_parts_mut": None,
        "get": None,
        "get_mut_unchecked": None,
        "get_unchecked": None,
        "get_unchecked_mut": None,
        "into": None,
        "into_raw": None,
        "into_raw_with_allocator": None,
        "len": None,
        "libc": None,
        "malloc": None,
        "new_unchecked": None,
        "new_uninit": None,
        "new_uninit_slice": None,
        "new": None,
        "new_in": None,
        "new_zeroed": None,
        "new_zeroed_slice": None,
        "offset": None,
        "offset_from": None,
        "set_len": None,
        "swap_unchecked": None,
        "split_at_unchecked": None,
        "split_at_mut_unchecked": None,
        "slice_unchecked": None,
        "sub": None,
        "transmute": None,
        "to_int_unchecked": None,
        "to_owned": None,
        "uninit": None,
        "uninit_array": None,
        "unwrap_unchecked": None,
        "unwrap_err_unchecked": None,
        "unwrap": None,
        "unchecked_mul": None,
        "unchecked_add": None,
        "wrapping_offset": None,
        "wrapping_add": None,
        "wrapping_sub": None,
        "write": None,
        "zeroed": None,
        "mem": None, 
        "key": None,
        "ptr": None,
        "self": None,
        "str": None,
    }
    
    if input_file.endswith('.ast'):
        # 打开原始文件和新文件
        with open(os.path.join(dir_path, input_file), 'r') as f1, open(os.path.join(dir_path, 'simplify_tree_' + input_file), 'w') as f2:
            # 逐行读取原始文件内容并写入新文件
            string = f1.read()
            string = re.sub('ident:[ \w]{1,}\([\n ]*([\w]{1,},)[\n ]*\),', 'ident: \g<1>', string, flags=re.S)
            # 将以"ident"开头的匹配项中的"ident"后面括号中的第一个单词后的逗号与括号中的内容替换为","
            string = re.sub('method:[ \w]{1,}\([\n ]*([\w]{1,},)[\n ]*\),', 'ident: \g<1>', string, flags=re.S)
            # # 将以"method"开头的匹配项中的"method"后面括号中的第一个单词后的逗号与括号中的内容替换为","
            string = string.replace('\n', '').replace(' ', '')
            # 去除所有换行符和空格
            string = string.replace("{", "(").replace("}", ")").replace("[", "(").replace("]", ")").lower()
            string = string.replace('(eq,', '( eq,').replace('(Mut,', '( Mut,') .replace('(Dot2,', '( Dot2,').replace('(Colon2,', '( Colon2,')
            result = re.findall('([()])|(ident:\w*)|([\w]*?token[\w]*?:[\w]*)|( eq,)|( Mut,)|( Colon2,)', string, flags=re.I)
            # 用正则表达式匹配出括号中的内容，并将结果连接为一个字符串
            result = [''.join(i).strip().strip(',') for i in result]
            # 将所有非括号的内容都用括号包起来，将结果连接为一个字符串
            result = [i if i in '()' else f'({i})' for i in result]
            output = ''.join(result)
            # 用正则表达式匹配出所有形如"(ident:xxx)"的内容，并将其中的变量名（即"xxx"）提取出来
            result = re.findall('\((ident:\w{1,})\)', output)
            # 将变量名没有出现在res_dict中的变量进行编号，然后将编号后的变量名放入一个字典di中，同时将变量名加入res_dict中
            filter_res = [i.split(':') for i in result if i.split(':')[-1] not in res_dict]
            di = {}
            for i in filter_res:
                if i[-1] not in di:
                    di[i[-1]] = 'var' + str(len(di) + 1)
                    res_dict[i[-1]] = None
            for k in di:
                output = output.replace('ident:' + k, 'ident:' + di[k])
            print("orgin_treeeeeeeee: ",output)
            print('-------------------------------------------------------------')

            output = re.sub(r'(brace_token:\s*Brace)|(semi_token:\s*Semi)|(paren_token:\s*Paren)|(pound_token:\s*Pound)|', "", output)
            token_find = re.findall(r'(([^\(\):]*token[^\(\):]*):([^\(\):]+))', output)
            for t, p, s in token_find:
                output = output.replace(t, p)
            ident_find = re.findall(r'(([^\(\):]*ident[^\(\):]*):([^\(\):]+))', output)
            for t, p, s in ident_find:
                output = output.replace(t, s)

            output = output.replace("()", "")

            print("orgin_tree: ", output)
            def simplify_bracket(src):
                stack= []
                splited = re.split(r"([\(\)])",src)
    #print(splited)
                for p in [e for e in splited if e]:
                    if p != ")":
                        stack.append(p)
                    else:
                        temp = ""
                        for i,_ in enumerate(range(len(stack))):
                            s_pop = stack.pop(-1)
                            if s_pop == "(":
                                if i <=1:
                                    if "(" not in temp:
                                        stack.append(f"({temp})")
                                    else:
                                        stack.append(temp)
                                else:
                                    stack.append(f'({temp})')

                                break
                            else:
                                temp = s_pop +temp
                return "".join(stack)

            print('-------------------------------------------------------------')
            simplify_tree = simplify_bracket(output)
            print("simplify_tree: ",simplify_tree)

            f2.write(simplify_tree)



