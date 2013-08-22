#!/usr/bin/ruby
# ruby 1.9 or 2.0 is required

guard 'bundler' do
  watch('Gemfile')
  # Uncomment next line if Gemfile contain `gemspec' command
  # watch(/^.+\.gemspec/)
end

guard :copy, from: 'archer/assets/js', to: 'archer/static/js/', mkpath: true do
  watch(%r{^.+\.js$})
end

guard :copy, from: 'archer/assets/css', to: 'archer/static/css/', mkpath: true do
  watch(%r{^.+\.css$})
end

guard :copy, from: 'archer/assets/img', to: 'archer/static/img/', mkpath: true do
  watch(%r{^.+\.png$})
end

guard :coffeescript, input: 'archer/assets/coffee', output: 'archer/static/js'

guard :sass, input: 'archer/assets/sass', output: 'archer/static/css'

# This will concatenate the javascript files specified in :files to public/js/all.js
guard :concat, type: 'js', files: %w(tree), input_dir: "archer/static/js/projects", output: "archer/static/js/projects"
guard :concat, type: 'js', files: %w(jquery-2.0.3 ajax), input_dir: "archer/static/js/core", output: "archer/static/js/core"

guard :concat, type: 'css', files: %w(custom_bootstrap), input_dir: 'archer/static/css/core', output: 'archer/static/css/core'
guard :concat, type: 'css', files: %w(tree actions), input_dir: 'archer/static/css/projects', output: 'archer/static/css/projects'

['archer/static/js/projects', 'archer/static/js/core'].each do |file|
  guard 'uglify', input: "#{file}.js", output: "#{file}.min.js" do
    watch ("#{file}.js")
  end
end

#['archer/static/css/projects'].each do |file|
#  guard 'minify', input: "#{file}.css", output: "#{file}.min.css"
#end

# like collectstatic
guard :shell do
  watch(%r{archer/static/.+\.(css|html|js|png)$}) do |m|
    `python manage-stfc-stratum-uploader.py collectstatic --noinput`
  end
end

guard 'livereload' do
  watch(%r{archer/static/.+\.(css|html|js|png)$})
  watch(%r{archer/.+\.(py)$})
  watch(%r{archer/.+/templates/.+/\.(html)$})
end

guard 'nosetests' do
  watch(%r{^archer/[a-z]+/tests.py$})
end
