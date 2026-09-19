package test.renamevar;

interface ConstantProvider {
    public static final int VALUE = 42;
}

class ParentClass {
    protected int fieldName = 0;
}

public class SourceClass3 extends ParentClass implements ConstantProvider {

    public void refMethod() {
        // Final local variable marked for renaming
        final int variableToBeRenamed = 10;
        
        // Anonymous inner class
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                // Local variable in the anonymous inner class's method
                int variableToBeRenamed = 20;

                // Accessing outer local variable
                System.out.println("Outer variable value: " + variableToBeRenamed);
                
                // Assigning a value to the inner local variable
                int innerVariable = fieldName + variableToBeRenamed;
                System.out.println("Inner variable value: " + innerVariable);
            }
        };
        runnable.run();
    }

    public void classMethod() {
        // Local variable marked for potential renaming
        int variableToBeRenamed = 5;
        
        // Accessing constant from the interface
        int result = VALUE + variableToBeRenamed;
        System.out.println("Result: " + result);
    }

    public static void main(String[] args) {
        SourceClass3 obj = new SourceClass3();
        obj.refMethod();
        obj.classMethod();
    }
}