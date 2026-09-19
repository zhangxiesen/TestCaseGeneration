package test.renamevar;

public class SourceClass1 {
    
    public void refMethod(int variableToBeRenamed, int anotherParam) {
    }
    
    public void externalMethod(int outerParam) {
        class InternalClass {
            private int outerParam;
            
            public void internalMethod() {
                this.outerParam = outerParam;
            }
        }
    }
}