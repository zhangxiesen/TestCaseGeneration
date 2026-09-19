package test.renamemethod;

public class SourceClass2 {

    public static void main(String[] args) {
        SourceClass2.InnerClass innerInstance = new SourceClass2.InnerClass();
        innerInstance.methodToBeRenamed();
    }

    private void privateHelperMethod() {
        System.out.println("This is a private helper method.");
    }

    public static class InnerClass {

        private String fieldName = "Inner field value";

        public void methodToBeRenamed() {
            System.out.println("Method executed: " + fieldName);
        }
    }
}