package test.renamefield;

public class SourceClass4 {
    private int fieldToBeRenamed;
    private String anotherField;
    private double yetAnotherField;

    public int getFieldToBeRenamed() {
        return fieldToBeRenamed;
    }

    public void setFieldToBeRenamed(int fieldToBeRenamed) {
        this.fieldToBeRenamed = fieldToBeRenamed;
    }
}

class TestClass {
    public void testMethod() {
        SourceClass4 source = new SourceClass4();

        // Create an anonymous class
        Runnable anonymousClass = new Runnable() {
            @Override
            public void run() {
                int localVariable = 42; // Renaming fieldToBeRenamed to localVariable
                source.setFieldToBeRenamed(localVariable);
                System.out.println("Field renamed to localVariable with value: " + source.getFieldToBeRenamed());
            }
        };

        // Execute the anonymous class
        anonymousClass.run();
    }
}