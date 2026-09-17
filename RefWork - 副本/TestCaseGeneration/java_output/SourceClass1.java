package test.renamemethod;

public class SourceClass1 {
    private void methodToBeRenamed() {
    }

    class InnerClass {
        void callMethod() {
            // cursor
            methodToBeRenamed();
        }
    }
}