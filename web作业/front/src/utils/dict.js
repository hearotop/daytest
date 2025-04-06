export const GENDER_MAP = {
  0: '男',
  1: '女'
};

export const formatter = (value, map) => {
  return map[value] || value;
};