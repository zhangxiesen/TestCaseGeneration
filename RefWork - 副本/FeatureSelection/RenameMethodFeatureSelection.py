import random
import os
import re
import csv
from typing import List, Dict


def build_refactoring_prompt(
    sample_id: int,
    refactoring_type: str,
    feature_pool: List[str],
    max_feature_cnt: int = 7
) -> Dict:
    pick_num = random.randint(1, max_feature_cnt)
    picked_features = random.sample(feature_pool, k=pick_num)

    source_cls = f"SourceClass{sample_id}"
    target_cls = f"TargetClass{sample_id}"

    description = f"""Task: Generate a complete, compilable Java program for refactoring engine testing. The target refactoring operation is: {refactoring_type}. Output only the Java source code with no extra text, descriptions or explanations. The generated Java program must satisfy all requirements in the Conditions and Features sections. Do not introduce any redundant logic beyond the required features."""

    conditions = f"""[Conditions]
    1. Source class name: {source_cls}
    2. The method name to be renamed: methodToBeRenamed
    3. The package name: test.renamemethod """

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
    max_feature: int = 7
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
  rename_method_feature = ["A class contains 'private' field",
       "Class contains getter and setter methods for  fields",
       "Rename the method to the new name of spock",
       "The method contains the 'native' modifier",
       "The class contains multiple privatization methods",
       "The parent class contains methods",
       " The method in the subclass is renamed to the parent class",
       "Methods that contain multiple different modifiers in the parent class",
       " Rename the method to another method name",
       "A class contains multiple methods of the same type",
       " Rename the method to another method name",
       "Methods that contain multiple different modifiers in the parent class",
       " Rename the method to another method name",
       "Methods that contain multiple different modifiers in the parent class",
       " Rename the method to another method name",
       "A class contains multiple methods of the same type",
       " The rename method is called in another class",
       " Rename a method to a method name that exists in another class",
       "The outer class has a private method which doesn't use a generic type parameter",
       " There is no interface defined here that involves defining a generic method",
       " The inner class isn't implementing an interface in the typical way described in the given context",
       "The class contains multiple privatization methods",
       " Rename the method to another method name",
       "The parent class contains methods",
       " An inner class in another class inherits the parent class",
       " A method in the inner class calls a method in the parent class",
       " Rename the method of the inner class to the method name of the parent class",
       "Rename the method to the 'private' modifier",
       "Classes contain inner classes",
       " The method in the inner class calls the rename method",
       " Rename the method to the method name in the inner class",
       "The method is the 'record' modifier",
       " The method is called by another type",
       "Subclasses inherit from external classes",
       " The method name is the same as the method name invoked by the external class",
       "The parent class defines inner classes and interfaces that establish functionality or contracts to be implemented or extended by subclasses",
       "Subclasses may define inner classes that implement interfaces or functionality defined in the parent class or other external interfaces",
       "Renaming methods in inner classes of subclasses can impact the implementation of interfaces or contracts, potentially requiring changes to method signatures or implementations in the subclass to ensure contract compliance",
       "The method is the 'record' modifier",
       " The method is called by another type",
       " The method is called in multiple places",
       "Declared with the abstract keyword",
       " A method without a body that must be implemented by subclasses",
       " Any subclass must implement the abstract method to become a concrete class",
       "The parent class contains multiple methods",
       " The method in the subclass and the renamed method in the parent class have the same formal parameter type",
       " Rename method calls exist in the parent class",
       " Rename the method to the method name in the subclass",
       "Methods are in abstract classes",
       " Rename the method to another method name",
       "The parent class contains multiple methods",
       " The method in the subclass and the renamed method in the parent class have the same formal parameter type",
       " Rename method calls exist in the parent class",
       " Rename the method to the method name in the subclass",
       "Methods are in abstract classes",
       " Rename the method to another method name",
       "This class defines a private instance variable, representing an identifier as a long",
       " It includes a public method that allows access to the value of the instance variable, ensuring encapsulation",
       " The method returns the current value of the identifier, allowing other classes to retrieve it without modifying the original value",
       " There are no constructors or additional methods beyond those mentioned, focusing solely on the identifier's retrieval",
       "The first class defines a public method, which serves as a placeholder for functionality in the superclass",
       "The method is called in multiple places",
       "A class contains multiple methods",
       " Rename the method to another method name",
       "A method in the parent class is called in the subclass",
       "The parent class contains internal classes and interfaces",
       " Subclasses contain inner classes that implement interfaces",
       " Rename the method name of the subclass's inner class",
       "A class contains local variable declarations",
       " An assignment statement contains fields assigned to local variables",
       " Rename the field to the local variable name",
       "The first class defines a public method, which serves as a placeholder for functionality in the superclass",
       " The second class extends the first class and overrides the method, potentially adding or modifying behavior",
       " The third class contains a method that creates an instance of the subclass and calls the overridden method",
       " This setup demonstrates basic inheritance and method overriding across different classes in separate plugins",
       "Rename the method contains @Deprecated annotation",
       "The parent class contains methods",
       " A method in the parent class is called in the subclass",
       " Rename the method to the parent method name",
       "The first class defines a method that accepts a string parameter, which can be used for various operations",
       " The subclass overrides this method, using a different parameter name to illustrate that method signatures can remain the same while allowing for specific implementations",
       " This example demonstrates the concept of inheritance and method overriding, allowing subclasses to customize behavior while maintaining the original method's signature",
       "The class doesn't have a method using a generic type parameter within its own method definitions",
       " There is no interface defined within this class that defines a generic method",
       " This class isn't in a situation where it's implementing an interface in the relevant context that follows the described pattern",
       "A class contains local variable declarations",
       " An assignment statement contains fields assigned to local variables",
       " Rename the field to the local variable name",
       "The parent class contains multiple methods",
       " The method in the subclass and the renamed method in the parent class have the same formal parameter type",
       " Rename method calls exist in the parent class",
       " Rename the method to the method name in the subclass",
       "Subclasses inherit from external classes",
       " The method name is the same as the method name invoked by the external class",
       "A class contains renamed fields and inner classes ",
       "The inner class contains additional field declarations ",
       " Methods in the inner class contain calls to renamed fields ",
       " Rename the field name to the field name in the inner class",
       "Subclasses inherit from external classes",
       " The method name is the same as the method name invoked by the external class",
       "A class contains renamed field and internal classes",
       " The inner class contains additional field declarations",
       " Rename the field name to the field name in the inner class",
       "The method is the 'record' modifier",
       " The method is called by another type",
       " The method is called in multiple places",
       "The interface extends a repository interface, providing basic operations for a specific entity type with a primary key of a numeric type",
       " A custom query method is defined using an annotation that allows for complex data retrieval beyond standard operations",
       " The query retrieves instances where a certain date condition is met, along with additional checks for active status and another boolean condition",
       " The method accepts a date parameter, which is annotated to be used in the query execution",
       " The method is designed to return a single instance of the specified type that matches the defined criteria, highlighting a focus on filtered retrieval based on specific business rules",
       "A class is defined with a constructor that creates an instance of another class",
       " Within the constructor, a method of the created instance is called, demonstrating interaction between two classes",
       " The method being called is defined as private in the second class, indicating restricted access and encapsulation",
       " The code highlights the relationship between the two classes, where one class relies on the functionality of the other through method invocation",
       " The use of a cursor comment suggests an emphasis on focusing on the specific method being called, possibly for debugging or analysis purposes"
       ]
  GENERATE_TOTAL = 5
  refactor_name = "rename method"
  OUTPUT_JAVA_DIR = "./gen_java_output"

  prompt_results = batch_generate_prompts(
    total_generate=GENERATE_TOTAL,
    refactoring_type=refactor_name,
    feature_pool=rename_method_feature,
    max_feature=5
  )

  # CSV字段列表（只选取需要的字段，避免多余key报错）
  fieldnames = [
    "sample_id",
    "refactoring_type",
    "pick_feature_count",
    "source_class",
    "target_class",
    "picked_features",
    "full_prompt"
  ]

  with open("rename_method_prompt_output.csv", "w", encoding="utf-8-sig", newline="") as f:
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

  print("🎉 CSV prompt 文件生成完成：rename_method_prompt_output.csv")

