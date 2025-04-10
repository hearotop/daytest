package com.example.demo.Class;
import lombok.*;


@Setter
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class Test {
    public String key;
    public String value;
    @Override
    public String toString() {
        return "Test{" +
                "name='" + key + '\'' +
                ", value='" + value + '\'' +
                '}';
    }
}
