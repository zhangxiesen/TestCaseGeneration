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
    2. The method name to be inlined: methodToBeInlined
    3. The package name: test.inline """

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
    inline_features = [
    "Inline method creates utility class instance and invokes number condition verification method.",
    "Inline nested utility class delegates logic to another utility class.",
    "Inline second utility class contains threshold checking condition methods.",
    "Inline static utility method checks if input exceeds defined value without instance creation.",
    "Inline utility method executes conditional actions based on threshold check result.",
    "Inline private access modifier encapsulates utility class internal methods.",
    "Inline method uses privatization approach.",
    "The method invoking inline method is public.",
    "Inline method is invoked from multiple locations.",
    "Inline method body is empty.",
    "Inline method body contains return value statement.",
    "The caller method invoking inline method is void.",
    "Inline method is generic.",
    "Inline method is privatization method.",
    "Inline SWT UI label is created with SWT.NONE style and azimuth text.",
    "Inline method checks integer level and returns boolean for all satisfied conditions.",
    "Inline method is invoked inside lambda expressions.",
    "Inline abstract class implements interface with single abstract method.",
    "Inline class encapsulates private text field and event update method.",
    "Inline main method initializes integer variable and prints formatted concatenated string.",
    "Inline abstract class does not implement interface inlinable method.",
    "Inline public class main method prints static field from Source class.",
    "Inline derived class constructor calls super constructor after string trimming processing.",
    "Inline class private numeric field is converted to string inside void method.",
    "Inline subclass inherits parent class and invokes parent method.",
    "Inline local variable stores result from another invoked method, with commented redundant assignment.",
    "Inline method prints console message after invoking helper method.",
    "Inline Swing method invokes asynchronous action via method reference on UI thread.",
    "Inline refactoring task inlines weigh() call inside getProximity and fixes generic type parameter mismatch.",
    "Inline generic comparison class implements compare method returning constant integer.",
    "Inline method accepts list collection parameter and iterates collection elements.",
    "Inline synchronized instance and static methods print console messages.",
    "Inline constructor calls private method immediately after instance creation.",
    "Inline private method accepts Runnable and implements recursive call via method reference.",
    "Inline class defines protected final instance variable initialized by constructor.",
    "Inline composition class accesses referenced class internal private method.",
    "Inline comparison class lacks meaningful comparison logic and triggers unchecked warning.",
    "Inline method initializes list collection and passes list to element processing method.",
    "Inline constructor prints object reference during instance initialization.",
    "Inline private guard clause method returns early when condition matches.",
    "Inline interface defines connect method with username password and default account connect method.",
    "Inline method checks token against predefined parameter tag array and resets matched token to null.",
    "Inline method reads lines from BufferedReader until empty line and prints non-empty lines.",
    "Inline helper method validates empty string and handles IOException for input reading.",
    "Inline outer class contains static inner classes and enum with multi-level inheritance.",
    "Inline method uses instanceof operator multiple times to branch return string result.",
    "Inline method converts parameter object to string via empty string concatenation.",
    "Inline Bug class first method calls second string method then invokes toString on result.",
    "Inline parameterized method refactoring moves external method call argument into method body and removes parameter.",
    "Inline read-only method calls Node getParent() without modification and is invoked by multiple callers.",
    "Inline class counter tracks side effects incremented after each method invocation.",
    "Inline private method prints counter and formats object string for side effect.",
    "Inline null check method invokes producer method only when input is non-null.",
    "Inline public doSomething method handles input object and exception logic.",
    "Inline base class returns fixed string value, descendant class extends base class.",
    "Inline method body contains comments lost after inline refactoring transformation.",
    "Inline factory class uses private constructor and static factory method for instance creation.",
    "Inline subclass invokes superclass method using super keyword.",
    "Inline collection initialization contains suppression annotation for unchecked warning.",
    "Inline descendant wrapper method calls inherited base class method.",
    "Inline main method invokes static helper method with null argument using static import.",
    "Inline Collections.sort sorts list with custom comparator and modifies list in-place.",
    "Inline builder pattern class uses static inner builder class for fluent object construction.",
    "Inline condition checking method provides boolean result for value getter method decision.",
    "Inline Spring Controller POST handler returns RedirectView and contains unused internal method call."
    ]

    GENERATE_TOTAL = 1
    refactor_name = "inline method"
    OUTPUT_JAVA_DIR = "./gen_java_output"

    prompt_results = batch_generate_prompts(
        total_generate=GENERATE_TOTAL,
        refactoring_type=refactor_name,
        feature_pool=inline_features,
        max_feature=6
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

    with open("inline_method_prompt_output.csv", "w", encoding="utf-8-sig", newline="") as f:
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

    print("🎉 CSV prompt 文件生成完成：inline_method_prompt_output.csv")


