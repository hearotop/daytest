package com.example.demo.Entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "users")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "user_id", nullable = false, unique = true)

    private int userId;
    @Column(name = "password", nullable = false, unique = false)
    private String password;
    @Column(name = "phone", nullable = false, unique = true)
    private String phone;
    @Column(name = "email", nullable = false, unique = true)
    private String email;
    @Column(name = "sex", nullable = false, unique = false)
    private int sex;
    @Column(name = "nickname", nullable = false, unique = false)
    private String nickName;


    public User(String password, String phone, String email, int sex, String nickName) {
        this.password = password;
        this.phone = phone;
        this.email = email;
        this.sex = sex;
        this.nickName = nickName;
    }

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
