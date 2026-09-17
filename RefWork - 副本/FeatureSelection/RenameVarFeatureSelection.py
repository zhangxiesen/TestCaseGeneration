import random
import os
import re
import csv
from typing import List, Dict


def build_refactoring_prompt(
    sample_id: int,
    refactoring_type: str,
    feature_pool: List[str],
    max_feature_cnt: int = 3
) -> Dict:
    pick_num = random.randint(1, max_feature_cnt)
    picked_features = random.sample(feature_pool, k=pick_num)

    source_cls = f"SourceClass{sample_id}"
    target_cls = f"TargetClass{sample_id}"

    description = f"""Task: Generate a complete, compilable Java program for refactoring engine testing. The target refactoring operation is: {refactoring_type}. Output only the Java source code with no extra text, descriptions or explanations. The generated Java program must satisfy all requirements in the Conditions and Features sections. Do not introduce any redundant logic beyond the required features."""

    conditions = f"""[Conditions]
    1. Source class name: {source_cls}
    2. the method name of the variable to be renamed: refMethod
    3. The variable name to be renamed: variableToBeRenamed
    4. The package name: test.renamevar """

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
    max_feature: int = 4
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
    rename_var_feature_pool = [
    "A Java 21 switch pattern matching expression contains pattern variables declared in case labels.",
    "User invokes Rename refactoring to rename an unused pattern variable to identifier ignored. There are multiple local variables in the method .",
    "A Java switch pattern matching expression contains a named pattern variable.",
    "User invokes Rename refactoring to rename the pattern variable to underscore _. The class includes a main method as the entry point of the program. A local variable is declared and initialized within the main method. The value of the variable is printed to the console using System.out.print. The variable is of a primitive data type (int). Method contains renaming local variables and list declarations . Renames local variable names to list object names",
    "A method is defined with parameters sharing the same names as the declared variables. The method operates independently of the external variables due to parameter shadowing. A method call is demonstrated, and the example suggests renaming the method for better clarity or refactoring. The code highlights a scenario of invoking methods with potentially updated names after refactoring.",
    "A method contains JDBC SQL string literal with database column name, and a local variable whose identifier matches the column name text inside string.",
    "User invokes Rename refactoring with replace all occurrences for the local variable.",
    "The refactoring incorrectly replaces matching text inside string literal. The database column name in SQL gets changed, causing runtime database query failure.",
    "The code defines a method that accepts two integer parameters. The method is empty, meaning it does not perform any operations within its body. The method has a clear and simple structure with basic parameter types.",
    "A statement contains renaming a variable assigned to a field.The method has a clear and simple structure with basic parameter types.",
    "The code defines a method that accepts two integer parameters. The method is empty, meaning it does not perform any operations within its body.Local variables are renamed to other variable names",
    "A class contains a single field of target type and a collection field of the same target type with plural naming convention.",
    "User invokes Rename refactoring on the target type.",
    "A class is defined with private member variables, each of which holds a reference to the same type. Getter and setter methods are provided for each member variable, allowing access and modification of their values. The member variables and method parameters share the same name as the type, which may lead to confusion. A refactoring task is suggested to rename the type and its references consistently across the code.",
    "Methods contain private fields accessed through getter and setter methods. Private fields have verbose naming conventions. No explicit type definition for the fields used. Getter and setter methods exhibit repetitive code patterns. Absence of a constructor for field initialization. No null checks in setter methods for input validation. Lack of comments or documentation within the class. Consistent method naming following Java conventions, but unclear variable meanings.",
    "Method contains a single local variable. Local variable has a concise and clear name. No visibility modifiers are applied to the method. Method does not return a value (void). Lack of comments or documentation explaining the method's purpose. The variable is declared but not used, indicating potential redundancy.",
    "Rename variable name invalid character",
    "A local variable is declared and referenced in code. String literals contain the same identifier text; one occurrence of the identifier is prefixed by escaped tab character inside string literal.",
    "User invokes Rename refactoring with search in strings enabled.",
    "Methods contain renamed variables and anonymous inner classes . Anonymous inner class as return value . Anonymous inner classes call local variables . Anonymous inner classes contain field declarations . Variables are renamed to field names in anonymous inner classes",
    "Rename variable to 'null'. A method contains the return statement.",
    "Code contains nested inner classes with multiple scopes. An outer local variable is referenced inside nested inner method, and the nested method declares a parameter whose identifier is chosen as new name for outer variable.",
    "User invokes Rename refactoring to rename outer local variable to the identifier used by inner method parameter.",
    "The code defines a method that accepts an object as a parameter. It uses a switch statement to check the type of the provided object. The case expression attempts to match an object type (Long), with a variable (l) bound to the value of the object. The code prints a message with the value of the object if it matches the case condition. A default case is included to handle any unmatched types, but it doesn't perform any specific action other than printing an empty line.",
    "Method contains rename variables . lambda expression in method . The variable is renamed to the variable name in the lambda expression",
    "A lambda expression declares parameters in collection iteration method call.",
    "User invokes Rename refactoring on lambda parameter and inspects suggested name candidates.",
    "The refactoring provides unusable suggested parameter names;",
    "Method contains rename variables . Methods contain class declarations . The variable is renamed to the class object name",
    "The scenario involves an inner class with a variable that is only used within the outer class. During renaming, the refactoring tool attempts to change all instances of the variable across the entire project, even outside the scope of the inner class. The tool incorrectly performs a global search and replace, not respecting the variable's local scope. The \"Exclude\" feature does not work as expected, failing to mark the parent nodes correctly, while individual lines are updated correctly when manually reviewed. The refactoring process loses track of variable scope, causing unintended changes outside the intended context.",
    "The method contains formal parameters . The variable name is renamed to the parameter name",
    "The method contains formal parameters . Arguments are called by multiple statements or expressions . Rename the parameter name",
    "Subclasses that inherit from the parent class contain renamed fields . Subclasses contain getter and setter methods for renamed fields . The subclass calls the method in the parent class",
    "A class that contains getter and setter methods for renaming fields . A statement contains parameter assignments to the renamed field",
    "The parent class contains renamed fields . A statement in a subclass contains a parameter assignment to a field . The field is renamed to the parameter name",
    "An interface contains a method . Implement interfaces in a class . Class contains renamed fields . The overwrite method contains a parameter assignment statement to a renamed field",
    "The code defines a method that accepts two integer parameters. The method doesn't perform any actions or contain any logic inside its body. The method signature is simple, consisting only of parameter types and names.",
    "User invokes Rename Class refactoring, which opens a subdialog for renaming associated variables.",
    "The subdialog lists multiple rows with identical original name and identical suggested new name for different variable occurrences.",
    "Method contains multiple calls to the rename parameter",
    "The code defines a class with a method that contains a local variable. The variable is declared within the method and given the same name as the class. The variable is not initialized or used within the method, meaning it serves no functional purpose in this context. The example highlights the potential for confusion when a local variable shares the same name as the class.",
    "A local variable is declared inside a method, and a comment within the same method contains matching identifier text.",
    "User invokes Rename refactoring on the local variable.",
    "The code defines a class with a method that accepts two parameters of the same data type. The method body is empty, meaning no operations or logic are performed within the method. The method's parameters are used to pass values into the method. The method does not return any value.",
    "A method declares multiple parameters with distinct identifiers.",
    "User invokes Rename refactoring on one parameter and chooses new identifier that is already used by another parameter of the same method.",
    "The refactoring precondition check fails to detect duplicate parameter name. Transformation proceeds and produces syntactically invalid code with duplicate parameter identifiers.",
    "A method contains multiple local variables A local rename to another variable name",
    "A class contains an instance field and a method with a parameter. The method assigns value to the instance field.",
    "User invokes Rename refactoring to rename the instance field to the same identifier used by the method parameter.",
    "The refactoring detects name shadowing conflict and shows warning message.",
    "A valid behavior-preserving transformation exists: qualify field access with this keyword to resolve shadowing.",
    "A class is defined with a member variable to hold an integer value. A method is provided to set the value of the member variable. The method takes an integer parameter and assigns it to the member variable, allowing for controlled modification of its state.",
    "Methods contain variables and inner classes . Internal classes contain field declarations . The inner class contains methods that rename variables assigned to fields . Rename the variable to the field name",
    "The code defines a class with a method containing a local variable that is declared as final. Inside the method, there's a nested inner class. This inner class has an instance variable and a method. The method of the inner class tries to access the local variable declared in the enclosing method. The local variable is marked as final, allowing it to be accessed inside the inner class method. The method of the inner class assigns the value of the final variable to its instance variable. This demonstrates how final local variables can be accessed from within a nested inner class.",
    "Methods contain renamed variables and anonymous inner classes. Anonymous inner class is used as a return value. Anonymous inner classes access local variables. Anonymous inner classes contain field declarations. Variables are renamed to field names within anonymous inner classes.",
    "The program contains an abstract class. The abstract class defines an abstract method. The abstract method has two parameters. The method is surrounded by an incomplete comment block, indicating potential refactoring or exclusion from some process.",
    "Methods contain variables and anonymous inner classes . Anonymous inner classes contain methods that rename variables and assign values to new variables . Rename the variable name to the variable name in anonymous class",
    "Classes contain fields . Method contains rename variables . Method contains field calls . Rename the variable to the field name",
    "Classes contain fields and static inner classes . Static inner classes contain field declarations . Method contains field calls from static inner classes . Rename the variable to the field name",
    "The program contains a class with an instance variable. The class contains a static nested class. The static nested class has its own static variable. The outer class method uses an incomplete comment block, potentially for exclusion or refactoring. The method in the outer class accesses the static variable of the nested static class. The method also uses an instance variable in a way that might be subject to renaming or modification.",
    "The program contains a class with a method. The method contains a local variable declaration. The local variable is surrounded by an incomplete comment block, potentially for exclusion or modification. The method contains a for loop that initializes a loop variable. The for loop does not have any logic inside the block, only the loop structure is present.",
    "The program contains a class with a method. The method contains a local variable, with the potential for refactoring or exclusion, indicated by an incomplete comment block. The method includes a for loop with multiple variables initialized in the loop header. The for loop has an empty condition and iteration section, suggesting the possibility of an infinite loop.",
    "The program contains a class with a method. The method declares a local variable, surrounded by an incomplete comment block indicating potential renaming or exclusion. The method calls itself recursively. The method includes a try-catch block, where a Throwable is caught and assigned to a local variable. The catch block handles the exception but does not contain any logic.",
    "The program contains a class with an instance variable and a method. The method includes a local variable with a potential for renaming or exclusion, indicated by an incomplete comment block. The method performs a method call (toString()) on an instance variable within the method. The instance variable is of type String.",
    "The program contains two classes, where one class extends another. The parent class contains an instance variable. The child class overrides a method that references the instance variable from the parent class. The method in the child class includes a local variable marked for potential renaming. The method assigns a value to the inherited instance variable from the parent class.",
    "The interface contains fields . Implement interface class methods that contain fields to assign values to new variables . Rename the variable to the field name",
    "The program contains a method with multiple local variables. One of the local variables is marked for potential renaming. The method returns a value, and the marked variable is part of the method's local variable declaration. The method includes both a single variable and a variable declaration with multiple variables in a single line.",
    "The program contains an interface and a class implementing that interface. The interface defines a constant (a static final variable). The implementing class contains a method with local variables. One of the local variables is marked for potential renaming. The method in the class accesses the constant from the interface through the class.",
    "The program contains an abstract class. The abstract class has an abstract method. The method has a parameter that is marked for potential renaming. The method does not have any other implementation or access to variables.",
    "The program contains an interface. The interface has a method signature. The method has a parameter that is marked for potential renaming. The method is abstract and does not contain an implementation.",
    "Method contains renaming variables and inner classes . An inner class method contains multiple variables . Internal class methods include renaming variables and assigning values to other variables . The variable is renamed to the variable name in the inner class method",
    "Classes contain fields . Methods contain inner classes and renamed variables . Calls to variables in inner classes .The variable is renamed to the field name",
    "The program contains a method within a class. The method has a parameter that is marked for renaming. The method contains a local variable that is marked for renaming. The method calls itself recursively (or invokes another method). The local variable is initialized with a value.",
    "The program defines a method within a class. The method contains a final local variable marked for renaming. The method creates an anonymous inner class. The anonymous inner class contains a method that defines a local variable. The anonymous inner class's method accesses the local variable from the outer method. A local variable in the anonymous inner class is assigned a value.",
    "The program defines a method that accepts a final parameter and a final local variable marked for renaming. An anonymous inner class is created within the method. The anonymous inner class defines its own method that accesses the final local variable from the outer method. The final local variable is used in calculations both within the outer method and the anonymous inner class's method. The outer method calls the method within the anonymous inner class, passing variables that affect the final value of the local variable.",
    "The method contains formal parameters . The variable is renamed to another parameter name",
    "A method contains multiple variables . The variable is renamed to another variable name",
    "Classes contain fields . Methods contain inner classes and renamed variables . Calls to variables in inner classes .The variable is renamed to the field name",
    "The parent class contains fields . Subclass methods contain field calls . Rename the variable to the field name",
    "Interface inclusion field . Implement the field assignment variable statement in the interface class method . Rename the variable to the field name",
    "Classes contain fields and inner classes . Internal class methods contain field assignment variable statements . Rename the variable to the field name",
    "External methods contain inner classes . Internal classes contain fields . The internal class method contains the external method parameter assignment field statement . Rename the parameter to the field name",
    "A class contains a field. The class defines an inner class. Inside a method in the inner class: A parameter is passed to the method. The method assigns a field from the outer class to the method parameter. The method returns a value.",
    "The class implements an interface. The interface contains a constant. The class defines a method that takes a parameter. Inside the method: The parameter is assigned a value from the constant defined in the interface. The method returns a value.",
    "The class inherits from another class. The class contains a method with a parameter. The method assigns a value to a field from the parent class. The method returns a value.",
    "External methods contain inner classes . Internal class methods contain statements that change external methods . Rename external method parameters to internal class method parameters",
    "The class contains fields . The method contains field calls . Rename the variable to a field name",
    "The class contains fields and static inner classes . The static class contains the same field name . Method contains static class field calls . The method contains formal parameters of the same type as the external class . Rename the parameter to a static class name",
    "The method contains a for statement . Rename the method parameters to the parameter names in the for statement",
    "The method contains a for statement . Rename the method parameters to the parameter names in the for statement",
    "The method contains a try-catch . Rename the method parameters to the parameter names in the try-catch statement",
    "The class contains fields . Rename the method parameter to the field name . Method contains static class field calls",
    "The parent class contains fields . Rename the parameter to a field name . Field calls in subclass methods",
    "The method contains multiple formal parameters . Rename the parameter to the parameter name",
    "The interface contains fields . The statement of the method that implements the interface class contains the field assignment variable . Rename the parameter to the field name",
    "The class contains fields, . Methods contain inner classes . Internal class call field . Rename the parameter to the field name",
    "The method contains multiple formal parameters . Rename the parameter to the parameter name",
    "The method contains variables . Rename the parameter to a variable name",
    "The method contains variables . Rename the parameter to a variable name",
    "External methods contain inner classes . The internal class contains fields and parameter calls of external methods . Rename the parameter to the field name",
    "The parent class contains fields . Subclasses contain field calls . Rename the parameter to the field name",
    "The parent class contains fields . Subclasses contain field calls . Rename the parameter to the field name",
    "The class contains fields and inner classes . The inner class contains fields for parameter copy to the statement",
    "A functional interface is assigned a lambda expression that operates on an input. The lambda expression takes an input and produces a result based on it. The result produced is a transformation of the input into a different type.",
    "The interface defines a method that takes a generic type as a parameter. A method accepts an instance of the interface with a specific type (e.g., Invoice or wildcard ?). The method can operate on different types by using either a specific type or a wildcard for flexibility.",
    "The class implements an interface with a defined method. The method in the implementation class takes two arguments, with descriptive names. The method performs an action or operation, although the details of the implementation are omitted",
    "A method that takes an integer parameter is defined within a class. Inside the method, a local variable is declared but not initialized. The method returns a fixed value, in this case, 0.",
    "The class contains fields and inner classes . The inner class contains fields for parameter copy to the statement",
    "A method is defined to iterate over an array of type Class. Inside the loop, a specific element from the array is retrieved. After the loop, a reference to the first element in the array is assigned to a variable. The methods of that element are fetched using a method retrieval function. A second loop iterates over the fetched methods and performs an action with them.",
    "A local variable is declared and initialized. The constant from the interface is assigned to the local variable. The method returns a value.",
    "A class contains a field. The class also defines an inner class. Inside a method in the inner class: A local variable is declared and initialized. A field from the outer class is assigned to the local variable. The method returns a value."
   ]
    GENERATE_TOTAL = 5
    refactor_name = "rename variable"
    OUTPUT_JAVA_DIR = "./gen_java_output"

    prompt_results = batch_generate_prompts(
        total_generate=GENERATE_TOTAL,
        refactoring_type=refactor_name,
        feature_pool=rename_var_feature_pool,
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

    with open("rename_var_prompt_output.csv", "w", encoding="utf-8-sig", newline="") as f:
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

    print("🎉 CSV prompt 文件生成完成：rename_var_prompt_output.csv")
