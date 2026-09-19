package test.renamevar;

import java.util.ArrayList;
import java.util.List;

public class SourceClass2 {
    private int singleValue;
    private List<Integer> multipleValues;

    public SourceClass2() {
        this.singleValue = 0;
        this.multipleValues = new ArrayList<>();
    }

    public int refMethod(int inputValue) {
        int variableToBeRenamed; // Declare but do not initialize

        class InnerClass1 {
            public void innerMethod1() {
                int newVariableName = inputValue; // Reference outer local variable
                class InnerClass2 {
                    public void innerMethod2(int variableToBeRenamed) { // New name for outer variable
                        System.out.println("Inner method parameter: " + variableToBeRenamed);
                    }
                }
                InnerClass2 inner2 = new InnerClass2();
                inner2.innerMethod2(newVariableName);
            }
        }
        InnerClass1 inner1 = new InnerClass1();
        inner1.innerMethod1();

        return 0; // Return fixed value
    }
}