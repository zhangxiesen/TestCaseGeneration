package test.renamefield;

public class SourceClass5 {

    private int field1;
    private String field2;

    private int fieldToBeRenamed; // Field to be renamed

    public SourceClass5(int field1, String field2, int fieldToBeRenamed) {
        this.field1 = field1;
        this.field2 = field2;
        this.fieldToBeRenamed = fieldToBeRenamed;
    }

    public int getField1() {
        return field1;
    }

    public void setField1(int field1) {
        this.field1 = field1;
    }

    public String getField2() {
        return field2;
    }

    public void setField2(String field2) {
        this.field2 = field2;
    }

    public int getFieldToBeRenamed() {
        return fieldToBeRenamed;
    }

    public void setFieldToBeRenamed(int fieldToBeRenamed) {
        this.fieldToBeRenamed = fieldToBeRenamed;
    }

    // Inner class accessing renamed field indirectly
    public class InnerClass {
        public int getRenamedFieldFromOuter() {
            return fieldToBeRenamed; // Accessing renamed field here
        }
    }

    // Inner interface definition
    public interface InnerInterface {
        void innerInterfaceMethod();
    }

    // Local method with variable influencing the inner class
    public void enclosingMethod() {
        int localField = 10;

        class LocalInnerClass {
            public void printLocalField() {
                System.out.println("Local field value from enclosing method: " + localField);
            }
        }

        LocalInnerClass localInner = new LocalInnerClass();
        localInner.printLocalField();
    }
}