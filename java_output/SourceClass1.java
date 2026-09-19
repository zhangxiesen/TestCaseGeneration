package test.renamemethod;

// External usage class for testing
public class ExternalUsageClass {
    public static void main(String[] args) {
        SourceClass1 source = new SourceClass1();
        String result = source.methodToBeRenamed("Hello from ExternalUsageClass!");
        System.out.println(result);

        SourceClass1.Subclass subclass = new SourceClass1.Subclass();
        String subclassResult = subclass.methodToBeRenamed("Hello from Subclass!");
        System.out.println(subclassResult);
    }
}

// Source class definition
public class SourceClass1 {
    private String instanceField = "InstanceFieldData";

    // Method to be renamed
    public String methodToBeRenamed(String input) {
        String localVariable = instanceField; // Assignment: field to local variable
        return localVariable + " | Message: " + input;
    }

    // Subclass definition
    public static class Subclass extends SourceClass1 {
        private String subclassField = "SubclassFieldData";

        @Override
        public String methodToBeRenamed(String input) {
            String localVariable = subclassField; // Assignment: field to local variable
            return localVariable + " | Subclass Message: " + input;
        }

        // Inner class implementing an interface
        public class InnerClass implements ExampleInterface {
            @Override
            public void exampleMethod() {
                System.out.println("InnerClass implementing ExampleInterface");
            }
        }
    }
}

// Example interface declaration
interface ExampleInterface {
    void exampleMethod();
}