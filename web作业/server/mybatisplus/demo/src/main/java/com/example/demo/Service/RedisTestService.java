package com.example.demo.Service;

import com.example.demo.Config.RedisConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class RedisTestService {

    private RedisTemplate<String, String> currentTemplate;

    @Autowired
    private RedisConfig redisConfig;

    @Autowired
    public RedisTestService(RedisConfig redisConfig) {
        this.redisConfig = redisConfig;
        this.currentTemplate = redisConfig.getRedisTemplateByDatabase(0); // 默认使用数据库 0
    }

    public void setDataBase(int num) {
        this.currentTemplate = redisConfig.getRedisTemplateByDatabase(num);
    }

    public String getTest(String key) {
        return currentTemplate.opsForValue().get(key);
    }

    public boolean setTest(Map<String, String> map) {
        if (map == null || map.isEmpty()) {
            throw new IllegalArgumentException("Map cannot be null or empty");
        }

        String key = map.keySet().iterator().next();
        String value = map.get(key);

        currentTemplate.opsForValue().set(key, value);

        String retrievedValue = currentTemplate.opsForValue().get(key);
        return retrievedValue != null && retrievedValue.equals(value);
    }

    public boolean updateTest(String key, String newValue) {
        if (key == null || key.isEmpty()) {
            throw new IllegalArgumentException("Key cannot be null or empty");
        }
        currentTemplate.opsForValue().set(key, newValue);
        String retrievedValue = currentTemplate.opsForValue().get(key);
        return retrievedValue != null && retrievedValue.equals(newValue);
    }

    public boolean deleteTest(String key) {
        return currentTemplate.delete(key);
    }

    public boolean renameKey(String oldKey, String newKey) {
        String value = getTest(oldKey);
        if (value != null) {
            deleteTest(oldKey);
            Map<String, String> map = new HashMap<>();
            map.put(newKey, value);
            return setTest(map);
        }
        return false;
    }

    public List<Map<String, String>> getAllCaches() {
        return currentTemplate.keys("*").stream().map(key -> {
            String value = currentTemplate.opsForValue().get(key);
            return Map.of("key", key, "value", value);
        }).collect(Collectors.toList());
    }
}