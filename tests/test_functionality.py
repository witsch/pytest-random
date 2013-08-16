import py, pytest

pytest_plugins = "pytester"


@pytest.fixture
def tests(testdir):
    # set up some sample tests

    # needs multiple directories
    testdir.tmpdir.ensure("__init__.py")

    # needs multiple files in a directory
    testdir.makepyfile(
        test_one="""
        def test_a():
            pass

        """,
        test_two="""
        def test_z():
            pass

        """)

    # needs mutliple plain tests in a file
    testdir.makepyfile(
        test_three="""
        def test_c():
            pass

        def test_b():
            pass

        """,
        test_four="""
        def test_y():
            pass

        def test_w():
            pass

        """
        )

    if pytest.__version__ < '2.3':
        # needs multiple test classes in a file
        testdir.makepyfile("""
            import pytest

            class TestGimmel(object):
                def test_q(self):
                    pass

                def test_o(self):
                    pass

                def test_n(self):
                    pass

            class TestAleph(object):
                def test_d(self):
                    pass

                def test_e(self):
                    pass

                def test_f(self):
                    pass
            """)
    else:
        # needs multiple test classes in a file
        # with fixtures
        testdir.makepyfile("""
            import pytest

            class TestGimmel(object):
                def test_q(self):
                    pass

                def test_o(self):
                    pass

                def test_n(self):
                    pass

            @pytest.fixture
            def dummy_fixture(request):
                pass

            class TestAleph(object):
                def test_d(self, dummy_fixture):
                    pass

                def test_e(self):
                    pass

                def test_f(self, dummy_fixture):
                    pass
            """)

    return testdir


def output(testdir, args='', with_seed=False):
    # run the sample tests & return their output and seed
    out = testdir.runpytest('--verbose', *args.split()).outlines
    tests = [line for line in out if line.startswith('test_')]
    assert len(tests) == 12     # there are 12 sample tests
    if with_seed:
        seedline, = [line for line in out if line.startswith(u'Tests are shuffled')]
        seed = int(seedline.split()[-1].strip('.'))
        return tests, seed
    else:
        return tests


@pytest.fixture
def expected_output(tests):
    # collect output for a standard, non-random run
    expected = output(tests, '-p no:random')
    return expected


class TestFunctionality(object):

    def test_tests_are_not_random(self, tests, expected_output):
        # do non-randomized run
        actual_output = output(tests)

        # compare to standard
        assert actual_output == expected_output


    def test_tests_are_random(self, tests, expected_output):
        # do randomized run & compare to standard
        actual_output = output(tests, '--random')
        assert actual_output != expected_output

        # do 10 randomized runs & campare to other randomized runs
        run_results = [actual_output, expected_output]
        for x in range(10):
            actual_output = output(tests, '--random')
            assert not actual_output in run_results
            run_results.append(actual_output)


    def test_seed_is_written_and_can_be_set(self, tests):
        # do randomized run & get the seed
        first_output, seed = output(tests, '--random', with_seed=True)
        # second run should be the same order
        second_output = output(tests, '--random --random-seed %d' % seed)
        assert first_output == second_output
        # third run with different seed should be different
        third_output = output(tests, '--random --random-seed %d' % (seed + 1))
        assert first_output != third_output


    def test_last_seed_is_reused(self, tests):
        # do randomized run
        first_output, first_seed = output(tests, '--random', with_seed=True)
        # second run should be the same order
        second_output, second_seed = output(tests, '--random --random-last', with_seed=True)
        assert first_output == second_output
        assert first_seed == second_seed


    # fixtures are in version 2.3 onward
    @pytest.mark.skipif("pytest.__version__ < '2.3'")
    def test_group_by_fixture(self, tests, expected_output):
        import re
        matcher = re.compile('(test_.) PASSED')
        # run a few times and check that test_d and test_f are always together
        for x in range(5):
            actual_output = output(tests, '--random --random-group')
            assert actual_output != expected_output
            indices = dict(
                [
                    (matcher.search(x).group(1), i)
                    for i, x in enumerate(actual_output)])
            assert abs(indices['test_d'] - indices['test_f']) == 1
        # now run without grouping and check that test_d and test_f can be apart from one another
        gathered_indices = set()
        for x in range(5):
            actual_output = output(tests, '--random')
            assert actual_output != expected_output
            indices = dict(
                [
                    (matcher.search(x).group(1), i)
                    for i, x in enumerate(actual_output)])
            gathered_indices.add(abs(indices['test_d'] - indices['test_f']))
        assert gathered_indices != set([1])
