# Web作业项目说明

## 项目结构
```
web作业/
├── front/            -- 前端项目(Vite+React)
│   ├── public/       -- 静态资源
│   ├── src/          -- 源代码
│   ├── package.json  -- 前端依赖管理
│   └── vite.config.js
│
└── server/           -- 后端服务(Spring Boot)
    └── mybatisplus/  -- MyBatis-Plus实现
        └── demo/
            ├── src/main/java/
            │   ├── com/example/demo/
            │   │   ├── Controller/   -- REST API接口
            │   │   ├── Service/      -- 业务逻辑层
            │   │   └── Config/       -- Redis配置
            │   └── resources/        -- 应用配置
            └── pom.xml               -- Maven依赖管理
```

## 技术栈
- **前端**：Vite + React
- **后端**：Spring Boot 2.x + MyBatis-Plus + Redis
- **数据库**：MySQL
- **缓存**：Redis Cluster

## 核心模块
1. 用户管理模块
   - RESTful API接口（/user/*）
   - MyBatis-Plus数据访问
   - Redis缓存实现（用户查询缓存）

2. 缓存服务模块
   - 多数据库切换支持
   - 键值操作API
   - 缓存监控端点

## 运行方式
### 前端
```bash
cd front
npm install
npm run dev
```

### 后端
1. 启动Redis服务
2. 配置application.yml数据库连接
```bash
mvn spring-boot:run
```

## 依赖要求
- Node.js ≥16.x
- Java 11+
- MySQL 8.x
- Redis 6.x