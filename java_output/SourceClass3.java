package test.renamemethod;

interface Renamable {
    void methodToBeRenamed(int value);
}

public class SourceClass3 implements Renamable {
    @Override
    public void methodToBeRenamed(int value) {
        System.out.println("Executing methodToBeRenamed in SourceClass3 with value: " + value);
    }
}

class SubClass extends SourceClass3 {
    @Override
    public void methodToBeRenamed(int value) {
        System.out.println("Overridden methodToBeRenamed in SubClass with value: " + value);
    }

    class InnerClass implements Renamable {
        @Override
        public void methodToBeRenamed(int value) {
            System.out.println("methodToBeRenamed implementation in InnerClass with value: " + value);
        }
    }
}