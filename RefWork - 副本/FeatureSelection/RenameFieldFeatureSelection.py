

import random
import os
import re
import csv
from typing import List, Dict


def build_refactoring_prompt(
    sample_id: int,
    refactoring_type: str,
    feature_pool: List[str],
    max_feature_cnt: int = 4
) -> Dict:
    pick_num = random.randint(1, max_feature_cnt)   # 随机选1~3个
    picked_features = random.sample(feature_pool, k=pick_num)

    source_cls = f"SourceClass{sample_id}"
    target_cls = f"TargetClass{sample_id}"

    description = f"""Task: Generate a complete, compilable Java program for refactoring engine testing. The target refactoring operation is: {refactoring_type}. Output only the Java source code with no extra text, descriptions or explanations. The generated Java program must satisfy all requirements in the Conditions and Features sections. Do not introduce any redundant logic beyond the required features."""

    conditions = f"""[Conditions]
    1. Source class name: {source_cls}
    2. The field name to be renamed: fieldToBeRenamed
    3. The package name: test.renamefield """

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
    max_feature: int = 3
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
    rename_field_feature_pool = [
        "The class contains a method which defines local variables and creates an anonymous inner class.",
        "The anonymous inner class has its own method that accesses a local variable from the enclosing method's scope.",
        "Changing the local variable in the enclosing method may affect the inner class method's access to it and potentially require code adjustments.",
        "Modifying the name or parameters of the method within the anonymous inner class can impact the overall functionality and behavior of the code.",
        "Altering the structure of the enclosing method can change the execution flow and interaction with the anonymous inner class, potentially leading to different outcomes.",
        "Replacing the anonymous inner class with another type of class requires proper adjustments regarding variable access and how it fits into the overall class structure.",
        "The use of a specific keyword on the local variable influences its mutability within the scope and also affects how the inner class method interacts with it.",
        "There exists a statement that contains a parameter assigned to the renamed field.",
        "The class defines a member variable of a specific type.",
        "The class has a method that accesses the member variable and performs an output operation using it.",
        "Changing the name of the member variable may affect the method's ability to access and use it properly, potentially requiring updates in the method's code to ensure correct functionality.",
        "Renaming the method within the class could impact the clarity of the code and how other parts of the program call or interact with this method.",
        "Altering the type of the member variable would likely require corresponding changes in the method to handle the new data type correctly, potentially involving different operations or type casting.",
        "Changing the implementation of the method, such as modifying the output format or adding additional logic, would affect the overall behavior of the class and how it presents information related to the member variable.",
        "If the class is extended by a subclass, the subclass might inherit the member variable and the method, and any changes made to them in the superclass could have implications for how the subclass uses or overrides them.",
        "A class contains a private renamed field.",
        "A class contains getter and setter methods for renaming fields.",
        "Rename the field annotated with Ruslan.",
        "The class contains a constructor.",
        "A class contains a protected renamed field.",
        "Rename a field using an anonymous class call in a method of another class.",
        "Include a local variable declaration in a method of another class.",
        "The field is renamed to the local variable name.",
        "Rename a field in a class that contains an inner class.",
        "The inner class contains additional field declarations.",
        "An assignment statement in the inner class contains the renamed field and the declared field in the inner class.",
        "Inner classes contain local variables.",
        "An assignment statement includes renaming fields and assigning local variables.",
        "The class contains setter methods for renaming fields.",
        "A class contains multiple fields.",
        "Rename the field to another field name in the class.",
        "A template struct is defined that can take any type as a parameter.",
        "The struct contains a member variable of the template type, allowing it to hold values of that type.",
        "This structure enables the creation of flexible data types that can be customized based on the type provided during instantiation.",
        "A class contains multiple private fields.",
        "A class contains multiple private fields of different types.",
        "A class contains renamed field and internal classes.",
        "Methods in the inner class contain calls to renamed fields.",
        "Rename the field name to the field name in the inner class.",
        "A class contains a renamed field of type int.",
        "The try-catch block contains changes to the renamed field.",
        "A class contains getter and setter methods for fields with the same name.",
        "Multiple methods in a class contain anonymous inner classes.",
        "Anonymous inner classes contain renaming field declarations.",
        "Multiple methods contain calls to fields in anonymous inner classes.",
        "A class contains local variable declarations.",
        "An assignment statement contains fields assigned to local variables.",
        "The parent class contains internal classes and interfaces.",
        "Subclasses contain inner classes that implement interfaces.",
        "Rename the method name of the subclass's inner class."
    ]

    GENERATE_TOTAL = 5
    refactor_name = "rename field"       # 改成你的重构类型
    OUTPUT_JAVA_DIR = "./gen_java_output"

    prompt_results = batch_generate_prompts(
        total_generate=GENERATE_TOTAL,
        refactoring_type=refactor_name,
        feature_pool=rename_field_feature_pool,
        max_feature=4
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

    with open("rename_field_prompt_output.csv", "w", encoding="utf-8-sig", newline="") as f:
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

    print("🎉 CSV prompt 文件生成完成：rename_field_prompt_output.csv")
