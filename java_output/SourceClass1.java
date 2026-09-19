package test.inline;

// Source class with the method to be inlined
public class SourceClass1 {
    public void execute() {
        HelperClass helper = new HelperClass();
        helper.performTask();
    }
}

// Helper class with private method that will be inlined
class HelperClass {
    public void performTask() {
        String result = methodToBeInlined();
        System.out.println(result);
    }

    private String methodToBeInlined() {
        return "Method Inlined!";
    }
}

// Composition class accessing the HelperClass
class CompositionClass {
    private HelperClass helper;

    public CompositionClass() {
        this.helper = new HelperClass();
    }

    public void execute() {
        helper.performTask();
    }
}

// Superclass with a method to be invoked using super
class SuperClass {
    protected void displayMessage() {
        System.out.println("Message from SuperClass");
    }
}

// Subclass invoking superclass method using super keyword
class SubClass extends SuperClass {
    @Override
    protected void displayMessage() {
        super.displayMessage();
        System.out.println("Message from SubClass");
    }
}

// Factory class with private constructor and static factory method
class Factory {
    private Factory() {
        // Private constructor
    }

    public static Factory createInstance() {
        return new Factory();
    }
}