package com.example.demo.Class;


import com.baomidou.mybatisplus.annotation.TableName;
import lombok.*;
import org.springframework.context.annotation.Bean;

// 假设这里根据MyBatis改动更新注解和方法调用，例如添加MyBatis相关注解

@Data
@TableName("users") // 映射到 users 表
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class User {
    

    private int userId;
  
    private String password;
 
    private String phone;
    private String email;
    private int sex;
    private String nickName;





    @Override
    public String toString() {
        return "User{" +
                "userId=" + userId +
                ", password='" + password + '\'' +
                ", phone='" + phone + '\'' +
                ", email='" + email + '\'' +
                ", sex=" + sex +
                ", nickName='" + nickName + '\'' +
                '}';

    }
}
