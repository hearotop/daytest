package com.example.demo.Controller;
import com.example.demo.Class.Test;
import com.example.demo.Service.RedisTestService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;
import java.util.List;

@RestController
@RequestMapping("/data")
public class RedisTestController {

    @Autowired
    private RedisTestService redisTestService;

    @GetMapping("/get")
    public ResponseEntity<String> getTest(String key) {
        redisTestService.setDataBase(2);
        return ResponseEntity.ok().body(redisTestService.getTest(key));

    }
    @PostMapping("/set")
    public ResponseEntity<Boolean> setTest(@RequestBody Test test) {
        redisTestService.setDataBase(2);
        Map<String, String> map = new HashMap<>();
        map.put(test.getKey(),test.getValue());
        if(redisTestService.setTest(map))
        {
            return ResponseEntity.ok().body(true);
        }
        return ResponseEntity.badRequest().body(false);

    }
    @PostMapping("/update")
    public ResponseEntity<Boolean> updateTest(@RequestBody Test test) {
        redisTestService.setDataBase(2);
        if(redisTestService.updateTest(test.getKey(), test.getValue()))
        {
            return ResponseEntity.ok().body(true);
        }
        return ResponseEntity.badRequest().body(false);
    }
    @PostMapping("/rename")
    public ResponseEntity<Boolean> renameKey(@RequestBody Map<String, String> request) {
        String oldKey = request.get("oldKey");
        String newKey = request.get("newKey");
        redisTestService.setDataBase(2);
        if(redisTestService.renameKey(oldKey, newKey)) {
            return ResponseEntity.ok().body(true);
        }
        return ResponseEntity.badRequest().body(false);
    }

    @GetMapping("/list")
    public ResponseEntity<List<Map<String,String>>> getAllCaches() {

        redisTestService.setDataBase(2);
        return ResponseEntity.ok().body(redisTestService.getAllCaches());
    }
    @PostMapping("/delete")
    public ResponseEntity<Boolean> deleteTest(@RequestBody Test test) {

        redisTestService.setDataBase(2);
        return ResponseEntity.ok().body(redisTestService.deleteTest(test.getKey()));
    }
}
