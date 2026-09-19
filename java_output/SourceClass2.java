package test.renamefield;

public class SourceClass2 {
    private String fieldToBeRenamed;

    public SourceClass2(String initialValue) {
        this.fieldToBeRenamed = initialValue;
    }

    public void outerMethod() {
        System.out.println("Outer method accessing field: " + fieldToBeRenamed);
        
        InnerClass innerInstance = new InnerClass();
        innerInstance.innerMethod();
        
        new Object() {
            void anonymousMethod() {
                System.out.println("Anonymous inner class accessing field: " + fieldToBeRenamed);
                String localVariable = fieldToBeRenamed;
                System.out.println("Local variable assigned: " + localVariable);
            }
        }.anonymousMethod();
    }

    private class InnerClass {
        public void innerMethod() {
            String localVariable = fieldToBeRenamed;
            System.out.println("Inner method accessing field: " + localVariable);
            
            new Object() {
                void anotherAnonymousMethod() {
                    System.out.println("Another anonymous inner class accessing field: " + fieldToBeRenamed);
                }
            }.anotherAnonymousMethod();
        }
    }

    public static void main(String[] args) {
        SourceClass2 instance = new SourceClass2("Initial Value");
        instance.outerMethod();
    }
}