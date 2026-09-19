package test.renamemethod;

public class SourceClass4 {
    private int value;

    public SourceClass4(int initialValue) {
        this.value = initialValue;
    }

    // Method to be renamed
    public record int methodToBeRenamed() {
        return value;
    }

    // Public method to access the instance variable ensuring encapsulation
    public int getValue() {
        return value;
    }
}