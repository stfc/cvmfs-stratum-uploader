#!/usr/bin/ruby
# ruby 1.9 or 2.0 is required

guard 'bundler' do
  watch('Gemfile')
  # Uncomment next line if Gemfile contain `gemspec' command
  # watch(/^.+\.gemspec/)
end

guard :copy, from: 'uploader/assets/js', to: 'uploader/static/js/', mkpath: true do
  watch(%r{^.+\.js$})
end

guard :copy, from: 'uploader/assets/css', to: 'uploader/static/css/', mkpath: true do
  watch(%r{^.+\.css$})
end

guard :copy, from: 'uploader/assets/img', to: 'uploader/static/img/', mkpath: true do
  watch(%r{^.+\.png$})
end

guard :coffeescript, input: 'uploader/assets/coffee', output: 'uploader/static/js'

guard :sass, input: 'uploader/assets/sass', output: 'uploader/static/css'

# This will concatenate the javascript files specified in :files to public/js/all.js
guard :concat, type: 'js', files: %w(countdown jquery.countdown), input_dir: "uploader/static/js/packages", output: "uploader/static/js/packages"
guard :concat, type: 'js', files: %w(tree), input_dir: "uploader/static/js/projects", output: "uploader/static/js/projects"
guard :concat, type: 'js', files: %w(jquery-2.0.3 ajax), input_dir: "uploader/static/js/core", output: "uploader/static/js/core"

guard :concat, type: 'css', files: %w(custom_bootstrap table), input_dir: 'uploader/static/css/core', output: 'uploader/static/css/core'
guard :concat, type: 'css', files: %w(form), input_dir: 'uploader/static/css/appsetup', output: 'uploader/static/css/appsetup'
guard :concat, type: 'css', files: %w(tree actions packages_list), input_dir: 'uploader/static/css/projects', output: 'uploader/static/css/projects'

['uploader/static/js/projects', 'uploader/static/js/packages', 'uploader/static/js/core'].each do |file|
  guard 'uglify', input: "#{file}.js", output: "#{file}.min.js" do
    watch ("#{file}.js")
  end
end

#['uploader/static/css/projects'].each do |file|
#  guard 'minify', input: "#{file}.css", output: "#{file}.min.css"
#end

# like collectstatic
guard :shell do
  watch(%r{uploader/static/.+\.(css|html|js|png)$}) do |m|
    `python manage-cvmfs-stratum-uploader.py collectstatic --noinput`
  end
end

guard 'livereload' do
  watch(%r{uploader/static/.+\.(css|html|js|png)$})
  watch(%r{uploader/.+\.(py)$})
  watch(%r{uploader/.+/templates/.+/\.(html)$})
end

guard 'nosetests' do
  watch(%r{^uploader/[a-z]+/tests.py$})
end
