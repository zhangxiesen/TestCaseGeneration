package test.renamemethod;

// Parent class
public class SourceClass5 {
    // Public method with multiple modifiers
    public synchronized void methodToBeRenamed() {
        System.out.println("Original method in SourceClass5");
    }
}

// Another class with an inner class
class AnotherClass {
    // Inner class that inherits the parent class
    class InnerClass extends SourceClass5 {
        // Method in inner class calls the renamed method in the parent class
        public void invokeRenamedMethod() {
            methodToBeRenamed(); // Call the method from the parent class
        }
    }
}