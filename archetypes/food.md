+++
tags = []
date = '{{ .Date }}'
description = ""
title = '{{ replace .File.ContentBaseName "-" " " | title }}'
[params]
    rating = 
    featuredImage = "images/food/{{ .File.ContentBaseName}}.jpg"
+++

## Rating
