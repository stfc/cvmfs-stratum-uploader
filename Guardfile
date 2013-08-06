#!/usr/bin/ruby
# ruby 1.9 or 2.0 is required

guard :shell do
  cmd = 'python ./test_manage.py test'
  watch(%r{^archer/(packages|projects)/(models|views|tests|admin)\.py$}) do |p|
    file = "archer.#{p[1]}.#{p[2]}"
    test_file = "archer.#{p[1]}"
    #n "#{file} changed", "Running #{test_file}", :pending
    run_cmd = "#{cmd} archer/#{p[1]}"
    result = system(run_cmd)
    puts result
    if result
      n file, "Success", :success
    else
      n file, "Failure #{test_file}", :failed
    end
  end
end

