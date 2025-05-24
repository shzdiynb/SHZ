import os

# 确保模板文件夹存在
os.makedirs('templates', exist_ok=True)

# 定义HTML模板
html_template = '''<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>中医药查询系统</title>
  <link rel="stylesheet" href="../static/css/all.min.css">
  <link rel="stylesheet" href="../static/css/main.css">
  <link rel="stylesheet" href="../static/css/responsive.css">
</head>
<body>
  <div class="page-title">
    <div class="title">
      <h2>{{{{herbs[{index}].a}}}}</h2>
    </div>
    <div class="link">
      <a href="index.html">Home</a>
      <i class="fas fa-slash"></i>
      <span class="page">{{{{herbs[{index}].a}}}}</span>
    </div>
  </div>

  <section class="career">
    <section class="about">
      <div class="box-container">
        <div class="content">
          <div class="heading">
            <div class="sub"><h2>{{{{herbs[{index}].a}}}} 性状</h2></div>
            <br>
            <span>带 &nbsp; 您 &nbsp; 发 &nbsp; 现 &nbsp; 中 &nbsp; 药</span>
          </div>
          <p>&nbsp;&nbsp;&nbsp {{{{herbs[{index}].g}}}} </p>
          <ul class="about-features">
            <li>
              <div class="text">
                <i class="fas fa-pencil-ruler"></i>
                <p>拼音：{{{{herbs[{index}].b}}}}</p>
              </div>
            </li>
            <li>
              <div class="text">
                <i class="fas fa-drafting-compass"></i>
                <p>拉丁名：{{{{herbs[{index}].c}}}}</p>
              </div>
            </li>
            <li>
              <div class="text">
                <i class="fas fa-building"></i>
                <p>所属科目：{{{{herbs[{index}].d}}}}</p>
              </div>
            </li>
            <li>
              <div class="text">
                <i class="fas fa-project-diagram"></i>
                <p>性味：{{{{herbs[{index}].h}}}} {{{{herbs[{index}].i}}}}</p>
              </div>
            </li>
            <li>
              <div class="text">
                <i class="fas fa-lightbulb"></i>
                <p>归经：{{{{herbs[{index}].k}}}}</p>
              </div>
            </li>
          </ul>
        </div>
        <div class="image">
          <img src="../static/picture/Intro.jpg" alt="Career-Image">
        </div>
      </div>
    </section>

    <div class="career-benefits">
      <div class="benefit-item">
        <i class="fas fa-money-bill-alt"></i>
        <div class="content">
          <h3>{{{{herbs[{index}].a}}}} 功效</h3>
          <p>{{{{herbs[{index}].j}}}}</p>
        </div>
      </div>
      <div class="benefit-item">
        <i class="fas fa-chalkboard-teacher"></i>
        <div class="content">
          <h3>{{{{herbs[{index}].a}}}} 产地</h3>
          <p>{{{{herbs[{index}].e}}}}</p>
        </div>
      </div>
      <div class="benefit-item">
        <i class="fas fa-project-diagram"></i>
        <div class="content">
          <h3>{{{{herbs[{index}].a}}}} 采摘时间</h3>
          <p>{{{{herbs[{index}].f}}}}</p>
        </div>
      </div>
    </div>
  </section>

  <footer class="footer">
    <div class="content">
      <p>Copyright &copy; Night</p>
    </div>
  </footer>

  <script src="../static/js/jquery.min.js"></script>
  <script src="../static/js/script.js"></script>
  <script src="../static/js/nav-link-toggler.js"></script>
</body>
</html>
'''

# 生成HTML文件
for i in range(403):
    file_content = html_template.format(index=i)
    with open(f'templates/file{i+1}.html', 'w', encoding='utf-8') as file:
        file.write(file_content)

print("HTML 文件生成完毕。")
