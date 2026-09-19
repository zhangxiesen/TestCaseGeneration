package test.renamefield;

public class SourceClass1 {
    private int fieldToBeRenamed;

    public SourceClass1(int fieldToBeRenamed) {
        this.fieldToBeRenamed = fieldToBeRenamed;
    }

    public int getFieldToBeRenamed() {
        return fieldToBeRenamed;
    }

    public void setFieldToBeRenamed(int fieldToBeRenamed) {
        this.fieldToBeRenamed = fieldToBeRenamed;
    }

    public class InnerClass {
        public void displayField() {
            int localVariable = fieldToBeRenamed;
            System.out.println("Local Variable: " + localVariable);
        }
    }

    public static void main(String[] args) {
        SourceClass1 instance = new SourceClass1(10);
        SourceClass1.InnerClass innerInstance = instance.new InnerClass();
        innerInstance.displayField();
    }
}