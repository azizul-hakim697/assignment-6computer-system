class VMTranslator:
    def vm_push(segment, offset):
        asm = []
        if segment == "constant":
            asm += [f"@{offset}", "D=A"]
        elif segment in ["local", "argument", "this", "that"]:
            base = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}[segment]
            asm += [f"@{base}", "D=M", f"@{offset}", "A=D+A", "D=M"]
        elif segment == "temp":
            asm += [f"@{5 + offset}", "D=M"]
        elif segment == "pointer":
            asm += [f"@{3 + offset}", "D=M"]
        elif segment == "static":
            asm += [f"@Static.{offset}", "D=M"]
        asm += ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        return "\n".join(asm)

    def vm_pop(segment, offset):
        asm = []
        if segment in ["local", "argument", "this", "that"]:
            base = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}[segment]
            asm += [f"@{base}", "D=M", f"@{offset}", "D=D+A", "@R13", "M=D"]
        elif segment == "temp":
            asm += [f"@{5 + offset}", "D=A", "@R13", "M=D"]
        elif segment == "pointer":
            asm += [f"@{3 + offset}", "D=A", "@R13", "M=D"]
        elif segment == "static":
            asm += [f"@Static.{offset}", "D=A", "@R13", "M=D"]
        asm += ["@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D"]
        return "\n".join(asm)

    def vm_add():
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D"

    def vm_sub():
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D"

    def vm_neg():
        return "@SP\nA=M-1\nM=-M"

    _label_counter = 0

    def _unique_label(base):
        VMTranslator._label_counter += 1
        return f"{base}{VMTranslator._label_counter}"

    def vm_eq():
        lbl_true = VMTranslator._unique_label("EQ_TRUE")
        lbl_end = VMTranslator._unique_label("EQ_END")
        return (
            "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n"
            f"@{lbl_true}\nD;JEQ\n"
            "@SP\nA=M-1\nM=0\n"
            f"@{lbl_end}\n0;JMP\n"
            f"({lbl_true})\n@SP\nA=M-1\nM=-1\n"
            f"({lbl_end})"
        )

    def vm_gt():
        lbl_true = VMTranslator._unique_label("GT_TRUE")
        lbl_end = VMTranslator._unique_label("GT_END")
        return (
            "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n"
            f"@{lbl_true}\nD;JGT\n"
            "@SP\nA=M-1\nM=0\n"
            f"@{lbl_end}\n0;JMP\n"
            f"({lbl_true})\n@SP\nA=M-1\nM=-1\n"
            f"({lbl_end})"
        )

    def vm_lt():
        lbl_true = VMTranslator._unique_label("LT_TRUE")
        lbl_end = VMTranslator._unique_label("LT_END")
        return (
            "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n"
            f"@{lbl_true}\nD;JLT\n"
            "@SP\nA=M-1\nM=0\n"
            f"@{lbl_end}\n0;JMP\n"
            f"({lbl_true})\n@SP\nA=M-1\nM=-1\n"
            f"({lbl_end})"
        )

    def vm_and():
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D"

    def vm_or():
        return "@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D"

    def vm_not():
        return "@SP\nA=M-1\nM=!M"

    def vm_label(label):
        return f"({label})"

    def vm_goto(label):
        return f"@{label}\n0;JMP"

    def vm_if(label):
        return "@SP\nAM=M-1\nD=M\n" f"@{label}\nD;JNE"

    def vm_function(function_name, n_vars):
        return ""

    def vm_call(function_name, n_args):
        return ""

    def vm_return():
        return ""
if __name__ == "__main__":
    import sys
    if(len(sys.argv) > 1):
        with open(sys.argv[1], "r") as a_file:
            for line in a_file:
                tokens = line.strip().lower().split()
                if(len(tokens)==1):
                    if(tokens[0]=='add'):
                        print(VMTranslator.vm_add())
                    elif(tokens[0]=='sub'):
                        print(VMTranslator.vm_sub())
                    elif(tokens[0]=='neg'):
                        print(VMTranslator.vm_neg())
                    elif(tokens[0]=='eq'):
                        print(VMTranslator.vm_eq())
                    elif(tokens[0]=='gt'):
                        print(VMTranslator.vm_gt())
                    elif(tokens[0]=='lt'):
                        print(VMTranslator.vm_lt())
                    elif(tokens[0]=='and'):
                        print(VMTranslator.vm_and())
                    elif(tokens[0]=='or'):
                        print(VMTranslator.vm_or())
                    elif(tokens[0]=='not'):
                        print(VMTranslator.vm_not())
                    elif(tokens[0]=='return'):
                        print(VMTranslator.vm_return())
                elif(len(tokens)==2):
                    if(tokens[0]=='label'):
                        print(VMTranslator.vm_label(tokens[1]))
                    elif(tokens[0]=='goto'):
                        print(VMTranslator.vm_goto(tokens[1]))
                    elif(tokens[0]=='if-goto'):
                        print(VMTranslator.vm_if(tokens[1]))
                elif(len(tokens)==3):
                    if(tokens[0]=='push'):
                        print(VMTranslator.vm_push(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='pop'):
                        print(VMTranslator.vm_pop(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='function'):
                        print(VMTranslator.vm_function(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='call'):
                        print(VMTranslator.vm_call(tokens[1],int(tokens[2])))

        




