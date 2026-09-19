package test.renamevar;

interface RenameInterface {
    int SOME_CONSTANT = 42;
    void setField(int variableToBeRenamed);
}

public class SourceClass4 implements RenameInterface {

    private int variableToBeRenamed;

    @Override
    public void setField(int variableToBeRenamed) {
        this.variableToBeRenamed = variableToBeRenamed;
    }

    public int getField() {
        return variableToBeRenamed;
    }

    public void refMethod(int variableToBeRenamed) {
        InnerClass inner = new InnerClass();
        inner.useField(variableToBeRenamed);
    }

    class InnerClass {
        public void useField(int variableToBeRenamed) {
            System.out.println("Inner class used field: " + variableToBeRenamed);
        }
    }
}