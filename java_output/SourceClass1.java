package test.move;

public class SourceClass1 {

    public void methodToBeMoved(TargetClass1 target) {
        System.out.println("Method from SourceClass1, called with parameter: " + target.getInfo());
    }

    // Nested class in SourceClass1
    class NestedClass {
        public void callMovedMethod(TargetClass1 target) {
            methodToBeMoved(target);
        }
    }
}

class TargetClass1 {
    private String info;

    public TargetClass1(String info) {
        this.info = info;
    }

    public String getInfo() {
        return info;
    }
}