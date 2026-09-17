import random
import os
import re
import csv
from typing import List, Dict


def build_refactoring_prompt(
    sample_id: int,
    refactoring_type: str,
    feature_pool: List[str],
    max_feature_cnt: int = 6
) -> Dict:
    pick_num = random.randint(1, max_feature_cnt)
    picked_features = random.sample(feature_pool, k=pick_num)

    source_cls = f"SourceClass{sample_id}"
    target_cls = f"TargetClass{sample_id}"

    description = f"""Task: Generate a complete, compilable Java program for refactoring engine testing. The target refactoring operation is: {refactoring_type}. Output only the Java source code with no extra text, descriptions or explanations. The generated Java program must satisfy all requirements in the Conditions and Features sections. Do not introduce any redundant logic beyond the required features."""

    conditions = f"""[Conditions]
    1. Source class name: {source_cls}
    2. the method name of the variable to be extracted: refMethod
    3. mark the expressions for extracting local variables that need to be executed with special symbols:/*EXTRACT*/
    4. The package name: test.extractvar """

    feature_text_lines = "\n".join([f"- {ft}" for ft in picked_features])
    features = f"""[Features]
{feature_text_lines}"""

    full_prompt = f"""===== PROMPT SAMPLE {sample_id} =====
[Description]
{description}

{conditions}

{features}"""

    return {
        "sample_id": sample_id,
        "refactoring_type": refactoring_type,
        "pick_feature_count": pick_num,
        "source_class": source_cls,
        "target_class": target_cls,
        "picked_features": picked_features,
        "Description": description,
        "Conditions": conditions,
        "Features": features,
        "full_prompt": full_prompt
    }


def batch_generate_prompts(
    total_generate: int,
    refactoring_type: str,
    feature_pool: List[str],
    max_feature: int = 6
) -> List[Dict]:
    result_list = []
    for sid in range(1, total_generate + 1):
        item = build_refactoring_prompt(
            sample_id=sid,
            refactoring_type=refactoring_type,
            feature_pool=feature_pool,
            max_feature_cnt=max_feature
        )
        result_list.append(item)
    return result_list


def extract_java_code(llm_response_text: str) -> str:
    pattern = re.compile(r"```java\s*(.*?)```", re.DOTALL)
    match = pattern.search(llm_response_text)
    if match:
        code = match.group(1)
    else:
        code = llm_response_text
    return code.strip()


def save_java_file(sample_id: int, llm_response_text: str, output_root_dir: str = "./gen_java_output"):
    os.makedirs(output_root_dir, exist_ok=True)
    java_code = extract_java_code(llm_response_text)
    filename = f"SourceClass{sample_id}.java"
    full_path = os.path.join(output_root_dir, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(java_code)
    print(f"✅ 已保存：{full_path}")
    return full_path

if __name__ == "__main__":
    extract_var_features = [
    "Method contains multiple variable declaration statements.",
    "Extract the new name of the expression as another variable name.",
    "Method takes integer parameter and calls itself recursively twice with same parameter.",
    "Recursive method returns integer parameter after recursive invocations.",
    "Incomplete scanner statement with unfinished user input logic.",
    "Method creates Object array initialized with current class instance this.",
    "Method instantiates new instance of the same class and assigns to local variable.",
    "Method uses ternary operator to assign local integer variable based on input parameter.",
    "Integer variable is declared without initialization before value assignment.",
    "Second integer variable copies value from first variable which is later set to 1.",
    "Local variable is initialized with expression containing assignment operation.",
    "Method defines local String variable initialized with string literal.",
    "Calling method invokes another integer-returning method and discards its return value.",
    "Method invokes integer-returning method inside code block without using returned result.",
    "Extract expression in the conditional statement of the for loop.",
    "Class has integer field to store temporary value.",
    "Method initializes local fixed value and assigns value to class integer field.",
    "Method intentionally throws NullPointerException without exception handling.",
    "Recursive method has no base case and may cause stack overflow.",
    "Local integer variable is initialized but never used or returned in method.",
    "Local integer variable is initialized to zero and reassigned the same zero value.",
    "Void method defines local integer variable initialized to zero with no further operations.",
    "Method defines local class without any members inside method scope.",
    "Public boolean field is toggled with redundant conditional logic.",
    "Public integer field has redundant self-assignments and conditional increment or decrement.",
    "Four conditional statements check integer field equals zero for early method return.",
    "Loop structure with single iteration and empty loop body.",
    "Method declares local variable with identical name as parameter causing name shadowing compile error.",
    "Loop counter initialized to zero, condition runs while less than one with empty body.",
    "For loop has two counters, second counter starts at 17 and loop never executes.",
    "Method contains nested loops, outer loop increments counter inside print statement.",
    "Method returns unchanged integer parameter, infinite for loop calls this method and ignores return value.",
    "Class defines public static final constant with value 17.",
    "Method prints static constant from another Test class via class name access.",
    "Class contains instance variable initialized to 17, method prints this instance variable.",
    "Outer class method prints static constant defined inside static inner class.",
    "Method integer parameter annotated with @SuppressWarnings to suppress compiler warnings.",
    "Method has uninitialized unused local variable inside void method.",
    "Method intended to return Object missing return type declaration causing compile error.",
    "Parameterless recursive method with no termination condition triggers StackOverflowError.",
    "Extract the expression in the return value statement.",
    "Extract expressions containing anonymous class declarations.",
    "Class has static Object field, factory method missing return type declaration.",
    "Method contains multiple assignment statements.",
    "The new variable name is another variable name.",
    "Two integer fields, second field initializes using value of first field.",
    "No-arg constructor chains to parameterized constructor with expression 1+1.",
    "Instance variable initialized with arithmetic expression, constructor chaining supported.",
    "Class defines static final constant, method retrieves static constant value.",
    "Method initializes local Object variable to null.",
    "Class field stores lambda expression implementing Consumer<Integer>.",
    "Method uses try-with-resources with FileReader and reads characters from file.",
    "String variable initialized to foo, code extracts multiple substrings by incrementing index.",
    "Create string list via Arrays.asList and print list size to console.",
    "Method invokes bounded generic method with null and constant integer arguments.",
    "Random generator initialized with fixed seed, two nextLong calls produce identical result.",
    "Random generator initialized with fixed seed, sequential nextLong calls generate deterministic sequence.",
    "Method accepts integer parameter followed by varargs string arguments.",
    "Main method passes lambda expression as argument to foo function.",
    "Dynamically allocate memory for pointer variable in C-style code.",
    "Define struct with integer member and constant struct instance with pointer reference.",
    "Pointer references struct containing two-dimensional array and accesses array element.",
    "Define enum type and assign enum constant to variable.",
    "Variable initialized to zero, conditional statement toggles variable value.",
    "Parameterless function invoked inside main function.",
    "Integer and char variable defined, switch statement branches based on char value.",
    "Concatenate string literal with variable and use escape sequence for formatted print output.",
    "Class has non-standard method name, subclass inherits and invokes base class method.",
    "Package-private void method with no access modifier.",
    "Inner class method captures local variable in Runnable lambda and invokes outer private method.",
    "Extract the expression as an array.",
    "Method contains multiple array value changes.",
    "Static logger instance used, lazy lambda for log message evaluation.",
    "Extract Variable refactoring may trigger naming conflict on variable extraction.",
    "Private method iterates two lists with multiple index variables and multi-condition loop.",
    "Method uses instanceof to check object type, performs casting and conditional value print.",
    "Retrieve value from map using specified key.",
    "Method defines local class, lambda inside local class references enclosing method variable.",
    "Extract Method refactoring on lambda code adds extra parameter for captured variable.",
    "Extract Parameter refactoring applied on local variable declaration.",
    "Extract Method refactoring causes duplicate local variable name compile error.",
    "Method contains local inner class, inner class creates anonymous inner class inside its method.",
    "Static method constructs multiple objects inside conditional block and checks map key existence.",
    "Extract expressions containing method calls.",
    "Ternary operator creates two identical anonymous inner class instances with duplicated task creation logic.",
    "Extract Variable refactoring applied on non-literal argument identifier of method invocation.",
    "Extract Variable refactoring on anonymous class expression inside ternary branch.",
    "Extract the expression in the return statement.",
    "Extract Variable refactoring converts chained static import expression to fully qualified class name.",
    "Static nested constant class defines private static final constant initialized to null.",
    "Extract Variable refactoring uses static inner class name as new variable identifier.",
    "Introduce Local Variable refactoring infers wider numeric type than original integer expression.",
    "Ternary operator instantiates object based on null check with duplicated anonymous factory logic.",
    "Extract the expression in the class declaration.",
    "Extract Variable refactoring automatically adds final modifier to newly created local variable.",
    "Private two-dimensional int array, public method uses IntStream to filter and return iterator.",
    "Class A main method prints member variable value and returns fixed result.",
    "Create immutable map and process entries using stream filter and forEach assertions.",
    "Generic method declares integer variable initialized to zero with no other operations.",
    "Private method uses switch expression to branch logic by object type and throw runtime exception.",
    "Main method calls static method with null argument, class has instance initializer calling same static method.",
    "Entry point method prints return value from another invoked method.",
    "Variable assigned from another variable, native database query executed on assigned variable.",
    "Generic method declares integer variable initialized to zero with no other operations."
   ]
    GENERATE_TOTAL = 1
    refactor_name = "extract variable"
    OUTPUT_JAVA_DIR = "./gen_java_output"

    prompt_results = batch_generate_prompts(
        total_generate=GENERATE_TOTAL,
        refactoring_type=refactor_name,
        feature_pool=extract_var_features,
        max_feature=5
    )

    fieldnames = [
        "sample_id",
        "refactoring_type",
        "pick_feature_count",
        "source_class",
        "target_class",
        "picked_features",
        "full_prompt"
    ]

    with open("extract_variable_prompt_output.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in prompt_results:
            csv_row = {
                "sample_id": row["sample_id"],
                "refactoring_type": row["refactoring_type"],
                "pick_feature_count": row["pick_feature_count"],
                "source_class": row["source_class"],
                "target_class": row["target_class"],
                "picked_features": "; ".join(row["picked_features"]),
                "full_prompt": row["full_prompt"]
            }
            writer.writerow(csv_row)

    print("🎉 CSV prompt 文件生成完成：extract_variable_prompt_output.csv")
