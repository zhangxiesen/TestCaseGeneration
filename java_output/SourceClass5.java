package test.renamevar;

interface RenamingInterface {
    int fieldInInterface = 42; // Field in interface
}

public class SourceClass5 {
    public void refMethod() {
        int fieldInInterface = RenamingInterface.fieldInInterface; // Variable name to be refactored
        System.out.println("Value of the variable: " + fieldInInterface);
    }

    private static class ExternalMethods {
        private int externalField;

        public ExternalMethods(int externalField) {
            this.externalField = externalField;
        }

        public void performOperation(int oldParameterName) { // Parameter to be refactored
            InnerClass inner = new InnerClass(oldParameterName); // Pass the parameter to the inner class
            inner.innerMethod();
        }

        private class InnerClass {
            private int externalField;

            public InnerClass(int externalField) { // Field to be refactored
                this.externalField = externalField; // Assign external parameter to field
            }

            public void innerMethod() {
                System.out.println("Inner field value: " + externalField);
            }
        }
    }

    public static void main(String[] args) {
        SourceClass5 source = new SourceClass5();
        source.refMethod();

        ExternalMethods external = new ExternalMethods(100);
        external.performOperation(50);
    }
}