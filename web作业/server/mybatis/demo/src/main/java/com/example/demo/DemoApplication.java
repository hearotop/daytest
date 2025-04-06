package com.example.demo;


import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.IOException;

@SpringBootApplication
// 修正：将错误的 @MapperScan 替换为正确导入的 @MapperScans
@MapperScan("com.example.demo.Mapper") // 指定Mapper接口所在的包路径
// 这里可以添加根据替换操作需要更新的配置和注解
public class DemoApplication {

    public static void main(String[] args) throws IOException {

        SpringApplication.run(DemoApplication.class, args);
    }

}
