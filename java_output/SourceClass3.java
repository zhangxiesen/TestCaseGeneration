package test.renamefield;

public class SourceClass3 {
    private String fieldToBeRenamed;

    public SourceClass3(String fieldToBeRenamed) {
        this.fieldToBeRenamed = fieldToBeRenamed;
    }

    public void testRenamingField() {
        String localVariable = "Original Value";

        Runnable inner = new Runnable() {
            @Override
            public void run() {
                // Accessing both the renamed field and the local variable.
                System.out.println("Field: " + fieldToBeRenamed);
                System.out.println("Local Variable: " + localVariable);
            }
        };

        inner.run();
    }

    public String getFieldToBeRenamed() {
        return fieldToBeRenamed;
    }

    public void setFieldToBeRenamed(String fieldToBeRenamed) {
        this.fieldToBeRenamed = fieldToBeRenamed;
    }

    public static void main(String[] args) {
        SourceClass3 obj = new SourceClass3("Initial Field Value");
        obj.testRenamingField();
    }
}